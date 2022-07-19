from typing import Dict, List, Any
import config

def get_post_msg(department_name: str) -> dict[str, dict[str, str | list[
    list[dict[str, str]] | list[dict[str, str]] | list[dict[str, str]] | list[dict[str, str]] | list[dict[str, str]] |
    list[dict[str, str]] | list[dict[str, str]] | list[dict[str, str]] | list[dict[str, str]] | list[
        dict[str, str] | dict[str, str]] | Any]]]:
    title = "X-Lab 入职提醒"
    content = [
        [{
            "tag": "text",
            "text": "Hello，欢迎宝贝加入X-lab！为了确保新成员人事信息完善以及让新成员更快了解实验室的运行模式，在正式完成入职之前,还需要完成以下事宜。"
        }
        ],
        [{
            "tag": "text",
            "text": "1.检查智能人事信息是否完善："
        }],
        [{
            "tag": "text",
            "text": "   1）是否在加入组织前已填写入职登记表，如已填写即已完善"
        }],
        [{
            "tag": "text",
            "text": "   2）若未填写入职登记表，进入飞书“工作台”——“智能人事”——“我”——“更多信息”进行完善，内容为“个人信息”板块的所有必填内容以及“材料附件”里的证件照。"
        }],
        [{
            "tag": "text",
            "text": "   1）2）两项确认无误后，向 @余奕 报备，内容为：（部门）**已完成入职并完善信息如有任何疑问，请联系人 @余奕 "
        }],
        [{
            "tag": "text",
            "text": "2.检查自己是否已加入各类基础群聊"
        }],
        [
            {
                "tag": "text",
                "text": "   飞书：部门飞书群以及实验室总群"
            }
        ],
        [
            {
                "tag": "text",
                "text": "   微信：是否在部门水群、总群“汪洋大海”"
            }
        ],
        [
            {
                "tag": "text",
                "text": "3.实验室重要文档："
            }
        ],
        [
            {
                "tag": "text",
                "text": "实验室全员必看（必看）："
            },
            {
                "tag": "a",
                "text": "实验室全员必看（必看）",
                "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnX6zQbVIRbSComQ7lv8sfsm?from=from_copylink"
            }
        ],
        [
            {
                "tag": "text",
                "text": "课内卷翻天（可看）："
            },
            {
                "tag": "a",
                "text": "课内卷翻天（可看）",
                "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnAW2fwczm3w6kdV8m4FuHTf"
            }
        ],
        [
            {
                "tag": "text",
                "text": "设计技术提升（设计部门资料，可看）："
            },
            {
                "tag": "a",
                "text": "设计技术提升（设计部门资料，可看）",
                "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnP6yEZjZanNsHH0k8L1tZ6d"
            }],
        [
            {
                "tag": "text",
                "text": "部门新人必看：",
            }
        ]
    ]

    content_of_business = [[
        {
            "tag": "text",
            "text": "运营团队必看："
        },
        {
            "tag": "a",
            "text": "运营团队必看",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnRKGLBwVQ2XO3EYR7lPeqXb"
        }
    ]]
    content_of_soft = [[
        {
            "tag": "text",
            "text": "软件技术团队运营："
        },
        {
            "tag": "a",
            "text": "软件技术团队运营",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcniL4yPkBKwXzhUy3tTyF73c"
        }
    ]]
    content_of_hard = [[
        {
            "tag": "text",
            "text": "硬件技术团队运营："
        },
        {
            "tag": "a",
            "text": "硬件技术团队运营",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnA3Hm7bYn1bYraqWQFNomJa"
        }
    ], [
        {
            "tag": "text",
            "text": "硬件设计交互组："
        },
        {
            "tag": "a",
            "text": "硬件设计交互组",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnw7Z0QQr0SbG8564tA32pQe"
        }
    ], [
        {
            "tag": "text",
            "text": "硬件技术积累："
        },
        {
            "tag": "a",
            "text": "硬件技术积累",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnAKC3EJlJSuSXNbi1vWrgUd"
        }
    ]]
    content_of_product = [[
        {
            "tag": "text",
            "text": "品牌团队帮助手册："
        },
        {
            "tag": "a",
            "text": "品牌团队帮助手册",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnUPJ5eZ41OC8zOHZQctjmEd?from=auth_notice&hash=e9e9ca59cf8d0c180916fa6088e3f483"
        }
    ]]
    content_of_design = [[
        {
            "tag": "text",
            "text": "设计部门新人入职必看："
        },
        {
            "tag": "a",
            "text": "设计部门新人入职必看",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcntPzIAleP6739jD18TWSbJf"
        }
    ], [
        {
            "tag": "text",
            "text": "设计资源："
        },
        {
            "tag": "a",
            "text": "设计资源",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcn2oW4lHlFUpsbgVo43KIjod"
        }
    ], [
        {
            "tag": "text",
            "text": "审美提升："
        },
        {
            "tag": "a",
            "text": "审美提升",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcnrsJQU0h8LG5B3QclXpLqIf"
        }
    ], [
        {
            "tag": "text",
            "text": "内训分享:"
        },
        {
            "tag": "a",
            "text": "内训分享",
            "href": "https://xn4zlkzg4p.feishu.cn/wiki/wikcne5R5X9dXvVbaFwZtztaoOf"
        }
    ]]

    content_by_dept_name = {
        config._cfg.get("dept_names")["Business"]: content_of_business,
        config._cfg.get("dept_names")["Software"]: content_of_soft,
        config._cfg.get("dept_names")["Hardware"]: content_of_hard,
        config._cfg.get("dept_names")["Product"]: content_of_product,
        config._cfg.get("dept_names")["Design"]: content_of_design
    }

    post = {
        "title": title,
        "content": content + content_by_dept_name.get(department_name)
    }

    msg = {
        "zh_cn": post
    }
    return msg
