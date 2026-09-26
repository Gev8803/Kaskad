/* ============================================================================
 * KASKAD GROUP — SHARED / COMPANY DATA (stats, partners, clients, values …)
 * Trilingual { hy, ru, en }.
 * ==========================================================================*/
window.DATA = window.DATA || {};

window.DATA.company = {
  contact: {
    address: {
      hy: "Բագրատունյաց 54/3, Երևան, Հայաստան",
      ru: "Багратуняц 54/3, Ереван, Армения",
      en: "Bagratunyats 54/3, Yerevan, Armenia"
    },
    phone: "+374 77 241 212",
    phoneLink: "+37477241212",
    email: "info@kaskadgroup.am",
    mapEmbed: "https://www.google.com/maps?q=Bagratunyats%2054%2F3%20Yerevan%20Armenia&output=embed"
  },

  /* Homepage / About statistics ----------------------------------------- */
  stats: [
    { value: 20,  suffix: "+", label: { hy: "տարվա փորձ", ru: "лет опыта", en: "years of expertise" } },
    { value: 100, suffix: "+", label: { hy: "իրականացված նախագիծ", ru: "реализованных проектов", en: "completed projects" } },
    { value: 5,   suffix: "",  label: { hy: "արտադրական հարթակ", ru: "производственных площадок", en: "production sites" } },
    { value: 30,  suffix: "+", label: { hy: "սպասարկվող տարածաշրջան", ru: "обслуживаемых регионов", en: "regions served" } }
  ],

  /* Company advantages --------------------------------------------------- */
  advantages: [
    { icon: "cycle",   title: { hy: "Ամբողջական ցիկլ", ru: "Полный цикл", en: "Full cycle" },
      text: { hy: "Նախագծումից մինչև օբյեկտի շահագործման հանձնում՝ մեկ պատասխանատու գործընկեր։", ru: "От проектирования до ввода объекта в эксплуатацию — один ответственный партнёр.", en: "From design to commissioning — one accountable partner." } },
    { icon: "factory", title: { hy: "Սեփական արտադրություն", ru: "Собственное производство", en: "In-house manufacturing" },
      text: { hy: "Սեփական գործարաններ՝ միջին լարման բաշխիչ սարքերի, վահանակների և հաշվիչների արտադրության համար։", ru: "Собственные заводы для производства РУ среднего напряжения, щитов и счётчиков.", en: "Own plants producing medium-voltage switchgear, boards and meters." } },
    { icon: "medal",   title: { hy: "Սերտիֆիկացված որակ", ru: "Сертифицированное качество", en: "Certified quality" },
      text: { hy: "Արտադրանքը համապատասխանում է ГОСТ, IEC և ISO 9001 ստանդարտներին։", ru: "Продукция соответствует стандартам ГОСТ, IEC и ISO 9001.", en: "Products comply with GOST, IEC and ISO 9001 standards." } },
    { icon: "globe",   title: { hy: "Միջազգային տեխնոլոգիաներ", ru: "Международные технологии", en: "International technology" },
      text: { hy: "Բելգիական DEBA-ի տեխնոլոգիա և առաջատար եվրոպական բաղադրիչներ։", ru: "Технология бельгийской DEBA и ведущие европейские комплектующие.", en: "Belgian DEBA technology and leading European components." } },
    { icon: "team",    title: { hy: "Փորձառու թիմ", ru: "Опытная команда", en: "Experienced team" },
      text: { hy: "Ինժեներներ, նախագծողներ և մոնտաժային բրիգադներ՝ էներգետիկ օբյեկտների փորձով։", ru: "Инженеры, проектировщики и монтажные бригады с опытом на энергообъектах.", en: "Engineers, designers and installation crews experienced on power facilities." } },
    { icon: "shield",  title: { hy: "Անվտանգություն և հուսալիություն", ru: "Безопасность и надёжность", en: "Safety & reliability" },
      text: { hy: "Փոքր չափսեր, մոնտաժի հեշտություն, շահագործման հուսալիություն և էկոլոգիական անվտանգություն։", ru: "Малые габариты, простота монтажа, эксплуатационная надёжность и экологическая безопасность.", en: "Compact footprint, easy installation, operational reliability and environmental safety." } }
  ],

  /* Partners / suppliers ------------------------------------------------- */
  partners: [
    { name: "ABB" }, { name: "Schneider Electric" }, { name: "Legrand" }, { name: "Hager" },
    { name: "DEBA" }, { name: "EKRA" }, { name: "MIRTEK" }, { name: "Elster Metronica" }
  ],

  /* Key clients ---------------------------------------------------------- */
  clients: [
    { name: { hy: "Հայաստանի բարձրավոլտ էլեկտրացանցեր", ru: "Высоковольтные электрические сети Армении", en: "High-Voltage Electric Networks of Armenia" } },
    { name: { hy: "Հայաստանի էլեկտրական ցանցեր", ru: "Электрические сети Армении", en: "Electric Networks of Armenia" } },
    { name: { hy: "Ռուսատոմ Սերվիս (Ռոսատոմ)", ru: "Русатом Сервис (Росатом)", en: "Rusatom Service (Rosatom)" } },
    { name: { hy: "Հայկական ԱԷԿ", ru: "Армянская АЭС", en: "Armenian NPP" } },
    { name: { hy: "Интер РАО խումբ", ru: "Группа Интер РАО", en: "Inter RAO Group" } },
    { name: { hy: "Россети", ru: "ПАО Россети", en: "Rosseti PJSC" } },
    { name: { hy: "Մոսկվայի մետրոպոլիտեն", ru: "Московский метрополитен", en: "Moscow Metro" } },
    { name: { hy: "Газпром", ru: "Газпром", en: "Gazprom" } }
  ],

  /* Company values ------------------------------------------------------- */
  values: [
    { icon: "bulb",   title: { hy: "Նորարարություն", ru: "Инновации", en: "Innovation" },
      text: { hy: "«Մենք նոր տեխնոլոգիաներ ենք ներդնում կյանք» — եվրոպական լուծումների կիրառում։", ru: "«Мы внедряем новые технологии в жизнь» — применение европейских решений.", en: "“We bring new technologies to life” — applying European solutions." } },
    { icon: "medal",  title: { hy: "Որակ", ru: "Качество", en: "Quality" },
      text: { hy: "Բարձր որակ, հուսալիություն և երկարակեցություն յուրաքանչյուր արտադրանքում։", ru: "Высокое качество, надёжность и долговечность в каждом изделии.", en: "High quality, reliability and durability in every product." } },
    { icon: "shield", title: { hy: "Անվտանգություն", ru: "Безопасность", en: "Safety" },
      text: { hy: "Անձնակազմի և սարքավորումների անվտանգությունը՝ առաջնահերթություն։", ru: "Безопасность персонала и оборудования — приоритет.", en: "Safety of personnel and equipment is a priority." } },
    { icon: "leaf",   title: { hy: "Էկոլոգիականություն", ru: "Экологичность", en: "Sustainability" },
      text: { hy: "Էկոլոգիապես անվտանգ արտադրություն և արդյունավետ էներգիայի կառավարում։", ru: "Экологически безопасное производство и эффективное управление энергией.", en: "Environmentally safe production and efficient energy management." } }
  ],

  /* Company history milestones ------------------------------------------ */
  history: [
    { year: "2005", text: { hy: "«Կասկադ-Էներգո»-ի հիմնադրում՝ որպես «Կասկադ» հոլդինգի ինժեներա-շինարարական ուղղություն։", ru: "Основание «Каскад-Энерго» как инженерно-строительного направления холдинга «Каскад».", en: "Kaskad-Energo founded as the engineering & construction arm of the Kaskad Holding." } },
    { year: "2010", text: { hy: "Կալուգայում ժամանակակից գործարանի գործարկում՝ Բելգիական DEBA-ի տեխնոլոգիայով միջին լարման սարքերի արտադրության համար։", ru: "Пуск современного завода в Калуге по технологии DEBA для производства РУ среднего напряжения.", en: "Launch of a modern plant in Kaluga using DEBA technology for medium-voltage switchgear." } },
    { year: "2016", text: { hy: "Հայաստանում խոշոր ենթակայանների վերակառուցում՝ «Ախթանակ» 220 կՎ և «Փուրակ» 35/6 կՎ։", ru: "Реконструкция крупных подстанций в Армении: «Ахтанак» 220 кВ и «Пурак» 35/6 кВ.", en: "Reconstruction of major substations in Armenia: Akhtanak 220 kV and Purak 35/6 kV." } },
    { year: "2019", text: { hy: "Խելացի հաշվառման զանգվածային ներդրում՝ Հայաստանում ~250 000 բաժանորդ, Ռուսաստանում 395 000+ հաշվառման կետ։", ru: "Массовое внедрение умного учёта: ~250 000 абонентов в Армении, 395 000+ точек учёта в России.", en: "Large-scale smart-metering rollout: ~250,000 subscribers in Armenia, 395,000+ metering points in Russia." } },
    { year: "2026", text: { hy: "Երեք ուղղությունների միավորում մեկ խմբում՝ Երևանում կենտրոնակայանով։", ru: "Объединение трёх направлений в единую группу с головным офисом в Ереване.", en: "Three divisions united into a single group headquartered in Yerevan." } }
  ]
};
