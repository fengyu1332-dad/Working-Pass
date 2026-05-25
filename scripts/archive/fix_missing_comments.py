from supabase import create_client

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

missing_comments = {
    "080710T": {
        "name": "人工智能",
        "xuefeng_comment": "人工智能是研究模拟人类智能的学科，是第四次工业革命的核心技术，被誉为'皇冠上的明珠'。人工智能的优点是：1）薪资水平在所有专业中名列前茅；2）就业前景广阔，各行各业都需要；3）是国家战略重点发展方向。这个专业的缺点是：1）学习难度极大，需要扎实的数学和编程基础；2）顶级岗位竞争极其激烈；3）技术更新快，需要持续学习。报考建议：1）985/211硕博是基本门槛，本科直接就业较难；2）顶会论文和竞赛成绩是核心竞争力；3）PyTorch和TensorFlow必须精通；4）AI+行业（医疗、金融、制造）复合更有竞争力；5）这个方向适合真正热爱技术的学生，不是为了追热点。"
    },
    "080717T": {
        "name": "海洋机器人",
        "xuefeng_comment": "海洋机器人是研究水下机器人设计控制的学科，是海洋强国战略催生的新兴交叉专业。海洋机器人的优点是：1）国家海洋战略带来发展机遇；2）技术壁垒高，竞争力强；3）可以往海洋工程、军工和科考方向发展。这个专业的缺点是：1）小众专业，行业规模有限；2）可能需要出海作业；3）人才培养体系还不完善。报考建议：1）对海洋和机器人有真实兴趣才能学下去；2）水下导航和作业技术是核心能力；3）可以往无人潜器和AUV方向发展；4）考研后就业层次更高；5）海洋工程公司和军工单位是就业目标。"
    },
    "080904K": {
        "name": "信息安全",
        "xuefeng_comment": "信息安全是研究网络攻防和数据保护的学科，是数字时代最稀缺的人才方向之一。信息安全的优点是：1）人才缺口巨大，供不应求；2）薪资水平较高，越老越吃香；3）可以往多个行业发展，就业面广。这个专业的缺点是：1）需要持续学习，技术更新快；2）工作压力大，责任重；3）部分岗位需要值夜班。报考建议：1）CTF比赛成绩和实战能力是核心竞争力；2）渗透测试和漏洞挖掘是最值钱的技术；3）CISP和CISSP等证书有加分作用；4）实战经验比学历更重要；5）这个方向适合真正热爱网络安全、有黑客精神的学生。"
    },
    "080910T": {
        "name": "数据科学与大数据技术",
        "xuefeng_comment": "数据科学与大数据技术是研究海量数据采集处理分析的学科，是数字时代最热门的技术方向之一。数据科学的优点是：1）就业前景广阔，各行各业都需要数据人才；2）薪资水平在技术类中属于上乘；3）是新兴学科，发展潜力大。这个专业的缺点是：1）课程跨度大，需要自学很多东西；2）数学和编程基础要求高；3）行业变化快，需要持续学习。报考建议：1）SQL是基本功，必须精通；2）Python和机器学习是核心竞争力；3）业务理解能力比纯粹的技术更重要；4）大数据技术（Hadoop、Spark、Flink）是加分项；5）数据分析师和数据科学家是主要就业方向。"
    },
    "030101K": {
        "name": "监狱学",
        "xuefeng_comment": "监狱学是研究监狱管理和罪犯矫正的学科，是法学类中的特殊专业。监狱学的优点是：1）就业有保障，司法联考是入警途径；2）属于公务员编制，工作稳定；3）竞争相对较小。这个专业的缺点是：1）工作环境特殊，有一定危险性；2）社会认知度不高；3）部分岗位需要值夜班。报考建议：1）身高、体能、体检有严格要求；2）司法联考是进入监狱系统的唯一途径；3）女生招生名额少，但竞争也相对较小；4）监狱警察工作稳定但有风险；5）适合喜欢稳定工作、不怕辛苦的学生报考。"
    }
}

def update_majors():
    print(f"Updating {len(missing_comments)} majors with missing xuefeng_comment...")
    for code, data in missing_comments.items():
        try:
            result = supabase.table('majors').update({'xuefeng_comment': data['xuefeng_comment']}).eq('code', code).execute()
            print(f"Updated: {code} {data['name']}")
        except Exception as e:
            print(f"Error updating {code}: {e}")

if __name__ == "__main__":
    update_majors()
    print("Done!")
