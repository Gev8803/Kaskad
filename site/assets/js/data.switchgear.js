/* ============================================================================
 * KASKAD GROUP — SWITCHGEAR DIVISION DATA
 * Source: kaskad-ts.ru (ООО «Каскад ТЕХНОЛОГИИ и СИСТЕМЫ»)
 * All strings are trilingual: { hy, ru, en }. `ru` is the authoritative
 * original; hy/en are professional translations.
 * Consumed by app.js (renderer). Loaded as a plain <script> so it works
 * over file:// without fetch/CORS.
 * ==========================================================================*/
window.DATA = window.DATA || {};

window.DATA.switchgear = {
  /* Product categories shown on the Switchgear page + Products page ------- */
  categories: [
    {
      id: "kd2",
      slug: "kd-2",
      image: "assets/img/switchgear/kd-2.jpg",
      voltage: "6–24 kV",
      current: { hy: "մինչև 1250 Ա", ru: "до 1250 А", en: "up to 1250 A" },
      name: { hy: "KD-2 մոդուլներ (ԿՌՈՒ)", ru: "Модули KD-2 (КРУ)", en: "KD-2 Modules (Switchgear)" },
      summary: {
        hy: "Ներքին տեղակայման փոքրածավալ մոդուլային ԿՌՈՒ միակողմ սպասարկմամբ՝ 6–24 կՎ լարման եռաֆազ 50 Հց հոսանքի ընդունման և բաշխման համար։",
        ru: "Малогабаритное модульное комплектное распределительное устройство (КРУ) внутренней установки одностороннего обслуживания для приёма и распределения электроэнергии переменного трёхфазного тока 50 Гц напряжением 6–24 кВ.",
        en: "Compact modular indoor switchgear (single-side maintenance) for receiving and distributing 3-phase 50 Hz power at 6–24 kV."
      },
      description: {
        hy: "KD-2 մոդուլային կառուցվածքը միավորում է միջին լարման համակարգերի բոլոր գործառույթները։ Կիրառվում է քաղաքային և արդյունաբերական ցանցերի բաշխիչ կետերում ու տրանսֆորմատորային ենթակայաններում, գյուղատնտեսության և երկաթուղային տրանսպորտի էլեկտրաֆիկացման համար։",
        ru: "Модульная конструкция KD-2 объединила все функции систем среднего напряжения. Применяется в распределительных пунктах и трансформаторных подстанциях городских и промышленных сетей, для электрификации объектов сельского хозяйства и железнодорожного транспорта. Конструкция представляет собой набор различных по назначению ячеек по принципу «модульных блоков».",
        en: "The KD-2 modular design unites all medium-voltage system functions. Used in distribution points and transformer substations of urban and industrial grids, and for electrification of agricultural and railway facilities. Built as a set of purpose-specific cells on a “modular block” principle."
      },
      /* individual cells within KD-2 */
      items: [
        { code: "KD-A",     name: { hy: "KD-A մոդուլ", ru: "Модуль KD-A", en: "KD-A cell" } },
        { code: "KD-AADt",  name: { hy: "KD-AADt մոդուլ", ru: "Модуль KD-AADt", en: "KD-AADt cell" } },
        { code: "KD-Ac",    name: { hy: "KD-Ac մոդուլ", ru: "Модуль KD-Ac", en: "KD-Ac cell" } },
        { code: "KD-AM",    name: { hy: "KD-AM մոդուլ", ru: "Модуль KD-AM", en: "KD-AM cell" } },
        { code: "KD-AV",    name: { hy: "KD-AV մոդուլ", ru: "Модуль KD-AV", en: "KD-AV cell" } },
        { code: "KD-C",     name: { hy: "KD-C մոդուլ", ru: "Модуль KD-С", en: "KD-C cell" } },
        { code: "KD-D",     name: { hy: "KD-D մոդուլ", ru: "Модуль KD-D", en: "KD-D cell" } },
        { code: "KD-D-500", name: { hy: "KD-D-500 մոդուլ", ru: "Модуль KD-D-500", en: "KD-D-500 cell" } },
        { code: "KD-DT",    name: { hy: "KD-DT մոդուլ", ru: "Модуль KD-DT", en: "KD-DT cell" } },
        { code: "KD-LK",    name: { hy: "KD-LK մոդուլ", ru: "Модуль KD-LK", en: "KD-LK cell" } },
        { code: "KD-LKB",   name: { hy: "KD-LKB մոդուլ", ru: "Модуль KD-LKB", en: "KD-LKB cell" } },
        { code: "KD-P",     name: { hy: "KD-P մոդուլ", ru: "Модуль KD-P", en: "KD-P cell" } },
        { code: "KD-SN",    name: { hy: "KD-SN մոդուլ", ru: "Модуль KD-SN", en: "KD-SN cell" } },
        { code: "KD-T",     name: { hy: "KD-T մոդուլ", ru: "Модуль KD-T", en: "KD-T cell" } },
        { code: "KD-Z",     name: { hy: "KD-Z մոդուլ", ru: "Модуль KD-Z", en: "KD-Z cell" } },
        { code: "KD-K",     name: { hy: "KD-K մոդուլ", ru: "Модуль KD-K", en: "KD-K cell" } }
      ],
      specs: [
        { label: { hy: "Անվանական լարում", ru: "Номинальное напряжение", en: "Rated voltage" }, value: "6 / 10 / 24 kV" },
        { label: { hy: "Անվանական հոսանք", ru: "Номинальный ток", en: "Rated current" }, value: { hy: "մինչև 1250 Ա", ru: "до 1250 А", en: "up to 1250 A" } },
        { label: { hy: "Հաճախություն", ru: "Частота", en: "Frequency" }, value: "50 Hz" }
      ]
    },
    {
      id: "kdw",
      slug: "kdw",
      image: "assets/img/switchgear/kdw.jpg",
      voltage: "6–20 kV",
      current: { hy: "630–3150 Ա", ru: "630–3150 А", en: "630–3150 A" },
      name: { hy: "KDW մոդուլներ (ԿՌՈՒ)", ru: "Модули KDW (КРУ)", en: "KDW Modules (Withdrawable Switchgear)" },
      summary: {
        hy: "Ներքին տեղակայման կասետային տիպի ԿՌՈՒ՝ 6–10 կՎ, 630–3150 Ա, մեկուսացված կամ փոխհատուցված չեզոքով ցանցերի համար։",
        ru: "Комплектные распределительные устройства (КРУ) внутренней установки кассетного типа для приёма и распределения электроэнергии 6–10 кВ, 630–3150 А в сетях с изолированной или компенсированной нейтралью.",
        en: "Withdrawable-type indoor switchgear (cassette design) for 6–10 kV, 630–3150 A networks with isolated or compensated neutral."
      },
      description: {
        hy: "KDW ԿՌՈՒ-ն բաղկացած է առանձին պահարաններից՝ կոմուտացիոն ապարատներով, չափիչ սարքերով, ավտոմատիկայի և պաշտպանության սարքերով։ Պահարանները պատրաստվում են բարձրորակ ցինկապատ պողպատից, արտաքին տարրերը՝ փոշեներկապատ։ Կիրառվող վակուումային անջատիչներ՝ BB/TEL, VD-4, ND-4, EVOLIS, LF։",
        ru: "КРУ серии KDW состоит из отдельных шкафов с коммутационными аппаратами, приборами измерения, устройствами автоматики и защиты. Шкафы изготовлены из высококачественной оцинкованной стали, наружные элементы окрашены методом порошкового напыления. Применяемые вакуумные выключатели — BB/TEL, VD-4, ND-4, EVOLIS, LF. Управление: местное, дистанционное и телемеханическое.",
        en: "The KDW switchgear consists of separate cabinets with switching devices, metering instruments, automation and protection. Cabinets are made of high-grade galvanized steel with powder-coated outer elements. Vacuum circuit breakers used: BB/TEL, VD-4, ND-4, EVOLIS, LF. Control: local, remote and telemechanical."
      },
      docs: [
        { label: { hy: "KDW նկարագրության PDF կատալոգ", ru: "PDF каталог описания модуля KDW", en: "KDW description PDF catalogue" }, href: "#" },
        { label: { hy: "KDW բնութագրերի PDF կատալոգ", ru: "PDF каталог характеристик KDW", en: "KDW specifications PDF catalogue" }, href: "#" }
      ],
      specs: [
        { label: { hy: "Անվանական լարում (գծային)", ru: "Номинальное напряжение (линейное)", en: "Rated voltage (line)" }, value: "6, 10, 20 kV" },
        { label: { hy: "Առավելագույն աշխ. լարում", ru: "Наибольшее рабочее напряжение", en: "Max working voltage" }, value: "7.2; 12; 24 kV" },
        { label: { hy: "Գլխ. շղթաների անվ. հոսանք", ru: "Номинальный ток главных цепей", en: "Rated main-circuit current" }, value: "630–3150 A" },
        { label: { hy: "Հավաքովի անվ. հոսանք", ru: "Ток сборных шин", en: "Busbar rated current" }, value: "1600–3150 A" },
        { label: { hy: "Անջատման հոսանք", ru: "Ток отключения выключателя", en: "Breaking current" }, value: "20; 25; 31.5 kA" },
        { label: { hy: "Ջերմային կայունություն (3վ)", ru: "Ток термической стойкости (3 с)", en: "Thermal withstand (3 s)" }, value: "20; 25; 31.5 kA" },
        { label: { hy: "Էլեկտրադինամիկ կայունություն", ru: "Электродинамическая стойкость", en: "Electrodynamic withstand" }, value: "51, 64, 81 kA" },
        { label: { hy: "Պաշտպանության աստիճան", ru: "Степень защиты", en: "Protection degree" }, value: "IP 4X" },
        { label: { hy: "Կլիմայական կատարում", ru: "Климатическое исполнение (ГОСТ 15150-69)", en: "Climatic version (GOST 15150-69)" }, value: "У3 (-45…+40 °C)" },
        { label: { hy: "Չափսեր L×B×H", ru: "Габариты L×B×H, мм", en: "Dimensions L×W×H, mm" }, value: "750×1750×2330" },
        { label: { hy: "Զանգված", ru: "Масса, не более", en: "Weight, max" }, value: "1000 kg" },
        { label: { hy: "Ծառայության ժամկետ", ru: "Срок службы", en: "Service life" }, value: { hy: "30 տարի", ru: "30 лет", en: "30 years" } }
      ]
    },
    {
      id: "kso-ktis",
      slug: "kso-ktis",
      image: "assets/img/switchgear/kso-ktis.jpg",
      voltage: "6–10 kV",
      current: { hy: "1000 Ա", ru: "1000 А", en: "1000 A" },
      name: { hy: "KSO/KTiS մոդուլներ", ru: "Модули КСО - КТИС", en: "KSO/KTiS Chambers" },
      summary: {
        hy: "Միակողմ սպասարկման հավաքովի խցիկներ (KSO/KTiS)՝ մինչև 10 կՎ, 50 Հց եռաֆազ հոսանքի ընդունման և բաշխման համար։",
        ru: "Камеры сборные одностороннего обслуживания серии КСО/КТиС для приёма и распределения электроэнергии трёхфазного переменного тока 50 Гц напряжением до 10 кВ.",
        en: "Single-side maintenance assembled chambers (KSO/KTiS) for receiving and distributing 3-phase 50 Hz power up to 10 kV."
      },
      description: {
        hy: "KSO/KTiS խցիկները նախատեսված են էլեկտրական ենթակայանների համալրման համար՝ մեկուսացված կամ փոխհատուցված չեզոքով ցանցերում։ Ամուր կմախքային մետաղական կառուցվածք՝ առջևի դռնով և կողային պատով, դիտման պատուհաններով։",
        ru: "Камеры КСО/КТиС предназначены для комплектования электрических подстанций в сетях с изолированной или компенсированной нейтралью. Представляют собой жёсткую каркасную металлическую конструкцию с передней дверью и боковой стенкой, с окнами для визуального наблюдения.",
        en: "KSO/KTiS chambers are designed to equip electrical substations in networks with isolated or compensated neutral. A rigid frame metal structure with a front door and side wall, fitted with inspection windows."
      },
      docs: [
        { label: { hy: "KSO/KTiS PDF կատալոգ", ru: "PDF каталог модулей КСО-КТИС", en: "KSO/KTiS PDF catalogue" }, href: "#" }
      ],
      specs: [
        { label: { hy: "Անվանական լարում", ru: "Номинальное напряжение", en: "Rated voltage" }, value: "6; 10 kV" },
        { label: { hy: "Առավելագույն աշխ. լարում", ru: "Наибольшее рабочее напряжение", en: "Max working voltage" }, value: "7.2; 12 kV" },
        { label: { hy: "Գլխ. շղթաների հոսանք", ru: "Ток главных цепей", en: "Main-circuit current" }, value: "1000 A" },
        { label: { hy: "Հավաքովի շինաների հոսանք", ru: "Ток сборных шин", en: "Busbar current" }, value: "1600–3150 A" },
        { label: { hy: "Անջատման հոսանք", ru: "Ток отключения", en: "Breaking current" }, value: "12.5; 20 kA" },
        { label: { hy: "Պաշտպանության աստիճան", ru: "Степень защиты", en: "Protection degree" }, value: "IP20, IP21" },
        { label: { hy: "Չափսեր", ru: "Габариты, мм", en: "Dimensions, mm" }, value: "800×940×2450" },
        { label: { hy: "Զանգված", ru: "Масса, не более", en: "Weight, max" }, value: "380 kg" },
        { label: { hy: "Ծառայության ժամկետ", ru: "Срок службы", en: "Service life" }, value: { hy: "30 տարի", ru: "30 лет", en: "30 years" } }
      ]
    },
    {
      id: "kd3",
      slug: "kd-3",
      image: "assets/img/switchgear/kd-3.jpg",
      voltage: "SF6 · до 24 kV",
      current: { hy: "630 Ա", ru: "630 А", en: "630 A" },
      name: { hy: "KD-3 մոդուլներ (SF6)", ru: "Модули KD-3 (элегаз SF6)", en: "KD-3 Modules (SF6)" },
      summary: {
        hy: "Միջին լարման էլեգազային (SF6) մեկուսացմամբ միակողմ սպասարկման հավաքովի խցիկներ՝ կոմպակտ, սահմանափակ տարածքի օբյեկտների համար։",
        ru: "Камеры сборные одностороннего обслуживания серии KD-3 с элегазовой (SF6) изоляцией — компактные, для объектов с ограниченной площадью.",
        en: "KD-3 single-side maintenance chambers with SF6 gas insulation — compact, for space-constrained facilities."
      },
      description: {
        hy: "KD-3-ը մոդուլային բլոկային կառուցվածք է՝ SF6 գազով մեկուսացմամբ։ RV53 եռադիրք բեռի անջատիչը՝ ներկառուցված հողանցման անջատիչով, հերմետիկացված է ողջ ծառայության ընթացքում։ Համապատասխանում է ГОСТ և IEC 62271-200 ստանդարտներին։ KD3+ տարբերակը ներառում է SV-53 ներքին աղեղի մարիչ (<50 մվ)։",
        ru: "KD-3 — модульная конструкция на блочном принципе с изоляцией газом SF6. Трёхпозиционный выключатель нагрузки RV53 со встроенным заземлителем герметизирован на весь срок службы. Соответствует ГОСТ и IEC 62271-200. Вариант KD3+ включает гаситель внутренней дуги SV-53 (<50 мс).",
        en: "KD-3 is a block-principle modular design with SF6 gas insulation. The RV53 three-position load-break switch with built-in earthing switch is sealed for life. Compliant with GOST and IEC 62271-200. The KD3+ variant includes the SV-53 internal-arc quencher (<50 ms)."
      },
      items: [
        { code: "KD3-A",  name: { hy: "Ներածող/ելանցող մալուխի խցիկ", ru: "Ячейка с выключателем нагрузки RV53", en: "Load-break cell (RV53)" } },
        { code: "KD3-A+", name: { hy: "Աղեղնամարիչով խցիկ", ru: "Ячейка с гасителем внутренней дуги", en: "Cell with internal-arc quencher" } },
        { code: "KD3-P",  name: { hy: "Ապահովիչներով խցիկ", ru: "Ячейка с плавкими предохранителями", en: "Fuse-protection cell" } },
        { code: "KD3-D",  name: { hy: "Վակուումային անջատիչով խցիկ", ru: "Ячейка с вакуумным выключателем", en: "Vacuum-breaker cell" } },
        { code: "KD3-C",  name: { hy: "Չափիչ խցիկ", ru: "Ячейка измерительная", en: "Metering cell" } },
        { code: "KD3-K",  name: { hy: "Ներածման խցիկ", ru: "Ячейка ввода", en: "Incoming cell" } }
      ],
      specs: [
        { label: { hy: "Մեկուսացում", ru: "Изоляция", en: "Insulation" }, value: "SF6" },
        { label: { hy: "Բեռի անջատիչ", ru: "Выключатель нагрузки", en: "Load-break switch" }, value: "RV53 / RV44" },
        { label: { hy: "Ստանդարտներ", ru: "Стандарты", en: "Standards" }, value: "ГОСТ, IEC 62271-200" }
      ]
    },
    {
      id: "bktp",
      slug: "bktp",
      image: "assets/img/switchgear/bktp.jpg",
      voltage: "20/0.4 kV",
      current: null,
      name: { hy: "ԲԿՏԵ (BKTP)", ru: "БКТП", en: "BKTP (Prefab Substation)" },
      summary: {
        hy: "Բլոկային կոմպլեկտ տրանսֆորմատորային ենթակայաններ (ԲԿՏԵ)՝ 20/0.4 կՎ։",
        ru: "Блочные комплектные трансформаторные подстанции (БКТП) 20/0,4 кВ.",
        en: "Prefabricated block transformer substations (BKTP) 20/0.4 kV."
      },
      description: {
        hy: "ԲԿՏԵ-ն ամբողջական գործարանային պատրաստվածության ենթակայան է՝ միջին լարումը ցածր լարման փոխակերպելու համար։",
        ru: "БКТП — трансформаторная подстанция полной заводской готовности для преобразования среднего напряжения в низкое.",
        en: "BKTP is a fully factory-assembled transformer substation converting medium voltage to low voltage."
      },
      items: [
        { code: "BKTP-20/0.4", name: { hy: "ԲԿՏԵ-20/0.4 կՎԱ", ru: "БКТП-20/0,4 кВА", en: "BKTP-20/0.4 kVA" } }
      ],
      specs: [
        { label: { hy: "Լարում", ru: "Напряжение", en: "Voltage" }, value: "20 / 0.4 kV" }
      ]
    },
    {
      id: "drives",
      slug: "privody",
      image: "assets/img/switchgear/privody.jpg",
      voltage: null,
      current: null,
      name: { hy: "Մեխանիկական շարժաբերներ", ru: "Механические приводы", en: "Mechanical Drives" },
      summary: {
        hy: "Բեռի անջատիչների և հողանցման անջատիչների մեխանիկական շարժաբերներ։",
        ru: "Механические приводы для выключателей нагрузки и заземлителей.",
        en: "Mechanical drives for load-break switches and earthing switches."
      },
      description: {
        hy: "DA և DP շարժաբերների շարք՝ միակի և կրկնակի գործառույթով, հարմարեցված KD-A, KD-P, KD-D, KD-K, KD-LK մոդուլներին։",
        ru: "Линейка приводов DA и DP с одинарной и двойной функцией, совместимых с модулями KD-A, KD-P, KD-D, KD-K, KD-LK.",
        en: "DA and DP drive range, single- and dual-function, compatible with KD-A, KD-P, KD-D, KD-K, KD-LK modules."
      },
      items: [
        { code: "DA-MEC",   name: { hy: "DA-MEC — կրկնակի գործառույթի շարժաբեր", ru: "DA-MEC — механический привод с двойной функцией", en: "DA-MEC — dual-function drive" } },
        { code: "DA-M-MEC", name: { hy: "DA-M-MEC — կրկնակի գործառույթի շարժաբեր", ru: "DA-M-MEC — привод с двойной функцией", en: "DA-M-MEC — dual-function drive" } },
        { code: "DA-K-MEC", name: { hy: "DA-K-MEC — միակի գործառույթի շարժաբեր", ru: "DA-K-MEC — привод с одинарной функцией", en: "DA-K-MEC — single-function drive" } }
      ],
      specs: []
    },
    {
      id: "components",
      slug: "components",
      image: "assets/img/switchgear/components.jpg",
      voltage: null,
      current: null,
      name: { hy: "Կոմպլեկտավորող տարրեր", ru: "Комплектующие", en: "Components" },
      summary: {
        hy: "Վակուումային անջատիչներ, բեռի անջատիչներ, հողանցման անջատիչներ և պաշտպանության ռելեներ։",
        ru: "Вакуумные выключатели, выключатели нагрузки, заземлители и реле защиты.",
        en: "Vacuum circuit breakers, load-break switches, earthing switches and protection relays."
      },
      description: {
        hy: "Մեխանիկական շարժաբերով վակուումային անջատիչներ՝ բաշխիչ սարքերի, տրանսֆորմատորների, գեներատորների և էլեկտրաշարժիչների կոմուտացիայի ու պաշտպանության համար։",
        ru: "Вакуумные выключатели с механическим приводом для коммутации и защиты распределительных устройств, трансформаторов, генераторов и электродвигателей.",
        en: "Vacuum circuit breakers with mechanical drive for switching and protecting switchgear, transformers, generators and motors."
      },
      items: [
        { code: "RV44",   name: { hy: "RV44 բեռի անջատիչ", ru: "Выключатель нагрузки RV44", en: "RV44 load-break switch" } },
        { code: "VA-2",   name: { hy: "VA-2 վակուումային անջատիչ", ru: "Вакуумный выключатель VA-2", en: "VA-2 vacuum circuit breaker" } },
        { code: "EM20",   name: { hy: "EM20 հողանցման անջատիչ", ru: "Заземляющий выключатель ЕМ20", en: "EM20 earthing switch" } },
        { code: "BB/TEL", name: { hy: "BB/TEL եռաֆազ վակուումային անջատիչ", ru: "Выключатель вакуумный трёхфазный ВВ/TEL", en: "BB/TEL three-phase vacuum breaker" } },
        { code: "RP-600", name: { hy: "RP-600 պաշտպանության ռելե", ru: "Реле защиты RP-600", en: "RP-600 protection relay" } }
      ],
      specs: []
    }
  ],

  /* Manufacturing / production narrative --------------------------------- */
  manufacturing: {
    hy: "Արտադրությունն իրականացվում է Կալուգայի ժամանակակից գործարանում՝ Բելգիական DEBA ընկերության տեխնոլոգիայով։ Հավաքումն իրականացվում է հայրենական և ներմուծվող կոմպլեկտավորող տարրերից՝ բարձր ճշգրտության սարքավորումների վրա։ Ամբողջ արտադրանքը սերտիֆիկացված է և համապատասխանում է ГОСТ և IEC ստանդարտներին։",
    ru: "Производство осуществляется на современном заводе в г. Калуга по технологии бельгийской компании DEBA. Сборка ведётся из отечественных и импортных комплектующих на высокоточном оборудовании. Вся продукция сертифицирована и отвечает как российским (ГОСТ), так и международным (IEC) стандартам.",
    en: "Manufacturing takes place at a modern plant in Kaluga using the technology of the Belgian company DEBA. Assembly uses domestic and imported components on high-precision equipment. All products are certified and comply with both Russian (GOST) and international (IEC) standards."
  },

  /* Certificates (gallery) ----------------------------------------------- */
  certificates: [
    { title: { hy: "ISO", ru: "ISO", en: "ISO" }, image: "assets/img/certs/iso.jpg" },
    { title: { hy: "ГАЗПРОМСЕРТ", ru: "СЕРТИФИКАТ ГАЗПРОМСЕРТ", en: "GAZPROMCERT" }, image: "assets/img/certs/gazprom.jpg" },
    { title: { hy: "KDW համապատասխանության սերտիֆիկատ", ru: "KDW — сертификат соответствия", en: "KDW conformity certificate" }, image: "assets/img/certs/kdw.jpg" },
    { title: { hy: "KD-3 համապատասխանության հայտարարագիր", ru: "Декларация о соответствии KD-3", en: "KD-3 declaration of conformity" }, image: "assets/img/certs/kd3.jpg" },
    { title: { hy: "KSO-KTiS համապատասխանության հայտարարագիր", ru: "Декларация о соответствии КСО-КТИС", en: "KSO-KTiS declaration of conformity" }, image: "assets/img/certs/kso.jpg" }
  ]
};
