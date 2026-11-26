import { defineConfig } from 'vitepress'

const ch = (folder: string, slug: string, text: string) => ({
  text,
  link: `/manuscript/${folder}/${slug}`
})

export default defineConfig({
  lang: 'zh-CN',
  title: '架构的代价',
  description: '互联网、物联网与智能体的六十六个判断点',
  // 本地与自托管用 '/'；GitHub Pages 项目页由 VITEPRESS_BASE 覆盖为 '/architecture-cost/'
  base: process.env.VITEPRESS_BASE || '/',
  cleanUrls: true,
  outDir: './site',
  lastUpdated: true,
  head: [
    ['meta', { name: 'author', content: '老苏' }],
    ['meta', { property: 'og:type', content: 'book' }],
    ['meta', { property: 'og:title', content: '架构的代价' }],
    ['meta', { property: 'og:description', content: '互联网、物联网与智能体的六十六个判断点' }]
  ],

  themeConfig: {
    nav: [
      { text: '目录', link: '/' },
      { text: '前言', link: '/manuscript/00-preface' },
      { text: '大纲', link: '/outline/03_全书大纲' },
      { text: '引用台账', link: '/references/' },
      { text: '关于作者', link: '/about' },
      {
        text: '参与',
        items: [
          { text: '写作规范', link: '/outline/00_写作规范与模板' },
          { text: '来源与引用规范', link: '/outline/01_案例来源与引用规范' },
          { text: '公开依据取证清单', link: '/outline/04_公开依据取证清单' }
        ]
      }
    ],

    sidebar: [
      {
        text: '序',
        items: [{ text: '前言：三种失败，一套判断', link: '/manuscript/00-preface' }]
      },
      {
        text: '第一篇 · 互联网',
        collapsed: false,
        items: [
          ch('01-internet', '01-orchestrator', '1　基座：编排器不听你的话'),
          ch('01-internet', '02-decision-language', '2　决策语言：五把尺子'),
          ch('01-internet', '03-request-failure', '3　服务端边界：一次请求的七种死法'),
          ch('01-internet', '04-client-budget', '4　客户端：预算是架构决策'),
          ch('01-internet', '05-incident-response', '5　生产现场：止血、定位、回滚')
        ]
      },
      {
        text: '第二篇 · 物联网',
        collapsed: true,
        items: [
          ch('02-iot', '06-online-illusion', '6　第一次握手：设备在线是幻觉'),
          ch('02-iot', '07-scale-cost', '7　规模：一万台设备的账'),
          ch('02-iot', '08-selection', '8　选型：先找结构性冲突'),
          ch('02-iot', '09-legacy', '9　存量：改造比新建难')
        ]
      },
      {
        text: '第三篇 · 智能体',
        collapsed: true,
        items: [
          ch('03-agent', '10-compounding-error', '10　复利：链路越长越不可靠'),
          ch('03-agent', '11-memory-space', '11　记忆与空间：让世界可读'),
          ch('03-agent', '12-agency', '12　代理权：谁能替谁做决定')
        ]
      },
      {
        text: '第四篇 · 安全',
        collapsed: true,
        items: [
          ch('04-security', '13-identity-boundary', '13　身份与边界：权限给多了才是常态'),
          ch('04-security', '14-key-data', '14　密钥与数据：加密不是算法问题'),
          ch('04-security', '15-physical-attack', '15　设备与现场：物理世界的攻击面'),
          ch('04-security', '16-supply-chain', '16　供应链与审计：每一层都在别人手里')
        ]
      },
      {
        text: '第五篇 · 合规',
        collapsed: true,
        items: [
          ch('05-compliance', '17-obligation-mapping', '17　义务识别：你到底适用哪些法'),
          ch('05-compliance', '18-data-lifecycle', '18　数据全生命周期：分级、最小必要、留存'),
          ch('05-compliance', '19-evidence-chain', '19　证据链：出事时你能拿出哪张纸')
        ]
      },
      {
        text: '第六篇 · 质量与测评',
        collapsed: false,
        items: [
          ch('06-quality-testing', '20-dfx-overview', '20　DFX 总论：设计同时锁定质量与成本'),
          ch('06-quality-testing', '21-dfm-dft', '21　可制造与可测试：DFM / DFT'),
          ch('06-quality-testing', '22-dfs-dfr', '22　可服务与可靠：DFS / DFR'),
          ch('06-quality-testing', '23-supply-quality', '23　供应链与在网质量：三个故障率'),
          ch('06-quality-testing', '24-three-criteria', '24　三套判据不可移植'),
          ch('06-quality-testing', '25-device-testing', '25　设备侧：型式检验、逐台出厂、批次抽检'),
          ch('06-quality-testing', '26-software-testing', '26　软件与智能体侧：测的是假设，不是功能'),
          ch('06-quality-testing', '27-review-acceptance', '27　评审与验收：谁签字，谁承担')
        ]
      },
      {
        text: '第七篇 · 成本与商业化',
        collapsed: false,
        items: [
          ch('07-commercial', '28-tco-structure', '28　TCO 的结构：五段成本，架构决定哪一段'),
          ch('07-commercial', '29-tco-control', '29　TCO 的把控：四种手段与它们改变的段'),
          ch('07-commercial', '30-cost-attribution', '30　成本与归属：Token 税与自研性价比'),
          ch('07-commercial', '31-quotation', '31　报价单即架构图'),
          ch('07-commercial', '32-delivery-warranty', '32　交付成本与维保责任'),
          ch('07-commercial', '33-qualification', '33　投标资格与替换成本')
        ]
      },
      {
        text: '收口',
        collapsed: false,
        items: [ch('07-commercial', '34-eight-lenses', '34　八个视角，六十六个判断点')]
      },
      {
        text: '附录',
        collapsed: false,
        items: [
          { text: '引用台账', link: '/references/' },
          { text: '关于作者', link: '/about' }
        ]
      }
    ],

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: {
            noResultsText: '没有找到结果',
            resetButtonTitle: '清除',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
          }
        }
      }
    },

    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一章', next: '下一章' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
    darkModeSwitchLabel: '主题',
    lastUpdatedText: '最后更新',
    footer: {
      message: '文字采用 CC BY-NC-SA 4.0 许可 · 欢迎指出错误',
      copyright: '© 2026 老苏'
    }
  }
})
