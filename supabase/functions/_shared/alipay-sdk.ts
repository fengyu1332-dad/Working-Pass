// ============================================================
// 支付宝 RSA2-SHA256 签名与验签
// 参考: https://opendocs.alipay.com/open/291/106097
//
// 密钥格式要求（Web Crypto API 原生支持）:
//   私钥: PKCS#8 PEM ("-----BEGIN PRIVATE KEY-----")
//   公钥: SPKI PEM  ("-----BEGIN PUBLIC KEY-----")
//
// PKCS#1 → PKCS#8 转换:
//   openssl pkcs8 -topk8 -inform pem -in rsa_key.pem -outform pem -nocrypt -out pkcs8_key.pem
// ============================================================

const ALGORITHM = "RSASSA-PKCS1-v1_5" as const;

function pemToArrayBuffer(pem: string): ArrayBuffer {
  const b64 = pem
    .replace(/-----[A-Z ]+-----/g, "")
    .replace(/\s/g, "");
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}

function isPkcs8(pem: string): boolean {
  return pem.includes("BEGIN PRIVATE KEY") && !pem.includes("RSA PRIVATE KEY");
}

function isPkcs1(pem: string): boolean {
  return pem.includes("BEGIN RSA PRIVATE KEY");
}

/**
 * 将 PKCS#1 DER 转换为 PKCS#8 DER
 * PKCS#8 = version(3) + AlgorithmIdentifier(15) + OCTET STRING wrapper
 */
function pkcs1ToPkcs8(pkcs1Der: ArrayBuffer): ArrayBuffer {
  const pkcs1Bytes = new Uint8Array(pkcs1Der);
  const algoId = new Uint8Array([
    0x30, 0x0d, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86,
    0xf7, 0x0d, 0x01, 0x01, 0x01, 0x05, 0x00,
  ]);

  // OCTET STRING 长度编码
  let octetHeader: number[];
  if (pkcs1Bytes.length < 0x80) {
    octetHeader = [0x04, pkcs1Bytes.length];
  } else if (pkcs1Bytes.length < 0x100) {
    octetHeader = [0x04, 0x81, pkcs1Bytes.length];
  } else if (pkcs1Bytes.length < 0x10000) {
    octetHeader = [0x04, 0x82, (pkcs1Bytes.length >> 8) & 0xff, pkcs1Bytes.length & 0xff];
  } else {
    octetHeader = [0x04, 0x83, (pkcs1Bytes.length >> 16) & 0xff, (pkcs1Bytes.length >> 8) & 0xff, pkcs1Bytes.length & 0xff];
  }

  const innerLength = 3 + algoId.length + octetHeader.length + pkcs1Bytes.length;
  let seqHeader: number[];
  if (innerLength < 0x80) {
    seqHeader = [0x30, innerLength];
  } else if (innerLength < 0x100) {
    seqHeader = [0x30, 0x81, innerLength];
  } else if (innerLength < 0x10000) {
    seqHeader = [0x30, 0x82, (innerLength >> 8) & 0xff, innerLength & 0xff];
  } else {
    seqHeader = [0x30, 0x83, (innerLength >> 16) & 0xff, (innerLength >> 8) & 0xff, innerLength & 0xff];
  }

  const version = [0x02, 0x01, 0x00];

  const totalLength = seqHeader.length + version.length + algoId.length + octetHeader.length + pkcs1Bytes.length;
  const result = new Uint8Array(totalLength);
  let offset = 0;

  // 诊断日志
  console.error(
    `[PKCS1→PKCS8] pkcs1Len=${pkcs1Bytes.length} ` +
    `innerLen=${innerLength}(0x${innerLength.toString(16)}) ` +
    `octetHdr=[${octetHeader.map(b=>'0x'+b.toString(16)).join(',')}] ` +
    `seqHdr=[${seqHeader.map(b=>'0x'+b.toString(16)).join(',')}] ` +
    `totalLen=${totalLength} ` +
    `pkcs1First4=[${Array.from(pkcs1Bytes.slice(0,4)).map(b=>'0x'+b.toString(16)).join(',')}] ` +
    `resultFirst10=[${seqHeader.map(b=>'0x'+b.toString(16)).join(',')},${version.map(b=>'0x'+b.toString(16)).join(',')},${algoId.slice(0,3).map(b=>'0x'+b.toString(16)).join(',')}]`
  );

  result.set(seqHeader, offset); offset += seqHeader.length;
  result.set(version, offset); offset += version.length;
  result.set(algoId, offset); offset += algoId.length;
  result.set(octetHeader, offset); offset += octetHeader.length;
  result.set(pkcs1Bytes, offset);

  return result.buffer;
}

async function importPrivateKey(pem: string, hash: "SHA-1" | "SHA-256"): Promise<CryptoKey> {
  // 先尝试直接当 PKCS#8 导入（容错：用户可能在 Dashboard 中直接粘贴了 PKCS#8 密钥）
  try {
    return await crypto.subtle.importKey("pkcs8", pemToArrayBuffer(pem), { name: ALGORITHM, hash }, false, ["sign"]);
  } catch (_) {
    // 如果不是有效 PKCS#8，继续走 PKCS#1 转换路径
  }

  if (isPkcs1(pem)) {
    const pkcs1Der = pemToArrayBuffer(pem);
    const pkcs1Bytes = new Uint8Array(pkcs1Der);
    console.error(`[importPrivateKey] pkcs1Der=${pkcs1Bytes.length}B, first8=[${Array.from(pkcs1Bytes.slice(0,8)).map(b=>'0x'+b.toString(16)).join(',')}]`);
    const pkcs8Der = pkcs1ToPkcs8(pkcs1Der);
    const pkcs8Bytes = new Uint8Array(pkcs8Der);
    console.error(`[importPrivateKey] pkcs8Der=${pkcs8Bytes.length}B, first8=[${Array.from(pkcs8Bytes.slice(0,8)).map(b=>'0x'+b.toString(16)).join(',')}]`);
    return crypto.subtle.importKey("pkcs8", pkcs8Der, { name: ALGORITHM, hash }, false, ["sign"]);
  }
  throw new Error("私钥格式不支持，请使用 PKCS#8 或 PKCS#1 PEM 格式");
}

async function importPublicKey(pem: string): Promise<CryptoKey> {
  return crypto.subtle.importKey("spki", pemToArrayBuffer(pem), { name: ALGORITHM, hash: "SHA-256" }, false, ["verify"]);
}

function buildSignContent(params: Record<string, string>): string {
  return Object.keys(params)
    .filter((k) => k !== "sign" && params[k] !== "" && params[k] !== null && params[k] !== undefined)
    .sort()
    .map((k) => `${k}=${params[k]}`)
    .join("&");
}

/**
 * 对支付宝请求参数进行 RSA2 签名，返回完整 query string
 *
 * 签名用 raw values（不编码），最终 URL 用 encoded values。
 * 参考: https://opendocs.alipay.com/open/291/106097
 */
export async function signAlipayParams(
  params: Record<string, string>,
  privateKeyPem: string,
): Promise<string> {
  const signType = params["sign_type"] || "RSA2";
  const hash = signType === "RSA" ? "SHA-1" : "SHA-256";
  if (!params["sign_type"]) params["sign_type"] = signType;

  // 1. 构建待签名字符串（raw values，不编码）
  const signContent = buildSignContent(params);
  const key = await importPrivateKey(privateKeyPem, hash);
  const signature = await crypto.subtle.sign(
    { name: ALGORITHM, hash },
    key,
    new TextEncoder().encode(signContent),
  );
  const signBase64 = btoa(String.fromCharCode(...new Uint8Array(signature)));

  // 2. 构建 URL query string（values 必须 URL-encode）
  const encodedQuery = Object.keys(params)
    .filter((k) => k !== "sign" && params[k] !== "" && params[k] !== null && params[k] !== undefined)
    .sort()
    .map((k) => `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
    .join("&");

  return `${encodedQuery}&sign=${encodeURIComponent(signBase64)}`;
}

/**
 * 验证支付宝异步通知签名
 */
export async function verifyAlipaySignature(
  params: Record<string, string>,
  alipayPublicKeyPem: string,
): Promise<boolean> {
  const sign = params["sign"];
  if (!sign) return false;

  const content = buildSignContent(params);
  try {
    const key = await importPublicKey(alipayPublicKeyPem);
    const signatureBytes = Uint8Array.from(atob(sign), (c) => c.charCodeAt(0));
    return crypto.subtle.verify(
      { name: ALGORITHM, hash: "SHA-256" },
      key,
      signatureBytes,
      new TextEncoder().encode(content),
    );
  } catch {
    return false;
  }
}
