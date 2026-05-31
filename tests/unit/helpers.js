import { vi } from 'vitest';

/**
 * Create a thenable mock for Supabase query chain.
 * Methods like .select()/.eq()/.order() return the chain itself.
 * When await-ed, resolves to the configured responseData.
 * .single()/.maybeSingle() are terminal and return Promises.
 */
export function mockQueryChain(responseData = { data: null, error: null }) {
  let currentResponse = responseData;

  const chain = {
    select: vi.fn(() => chain),
    eq: vi.fn(() => chain),
    neq: vi.fn(() => chain),
    gt: vi.fn(() => chain),
    gte: vi.fn(() => chain),
    lt: vi.fn(() => chain),
    lte: vi.fn(() => chain),
    order: vi.fn(() => chain),
    limit: vi.fn(() => chain),
    offset: vi.fn(() => chain),
    or: vi.fn(() => chain),
    ilike: vi.fn(() => chain),
    in: vi.fn(() => chain),
    insert: vi.fn(() => chain),
    upsert: vi.fn(() => chain),
    update: vi.fn(() => chain),
    delete: vi.fn(() => chain),
    set: vi.fn(() => chain),

    // Response control
    _setResponse: (res) => { currentResponse = res; },

    // Terminal: returns Promise directly
    single: vi.fn(() => Promise.resolve(currentResponse)),
    maybeSingle: vi.fn(() => Promise.resolve(currentResponse)),

    // Thenable: makes `await chain` work
    then: function (resolve, reject) {
      const r = currentResponse;
      if (r && r.error) return reject ? reject(r.error) : Promise.reject(r.error);
      return resolve ? resolve(r) : Promise.resolve(r);
    },
  };

  return chain;
}

/**
 * Create a mock Supabase client with auth, from(), rpc().
 */
export function mockSupabase(overrides = {}) {
  const defaultChain = mockQueryChain();

  const sb = {
    from: vi.fn(() => defaultChain),
    auth: {
      signInWithPassword: vi.fn(),
      signUp: vi.fn(),
      signOut: vi.fn(),
      getUser: vi.fn(),
      getSession: vi.fn(),
      onAuthStateChange: vi.fn(),
      resetPasswordForEmail: vi.fn(),
      updateUser: vi.fn(),
      signInWithOAuth: vi.fn(),
      admin: {
        deleteUser: vi.fn(),
      },
    },
    rpc: vi.fn(),
    ...overrides,
  };

  return sb;
}
