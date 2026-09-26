/* ============================================================================
 * KASKAD GROUP — ELECTRICITY METER DIVISION DATA
 * Source: mirtekgroup.com (brand МИРТЕК) — ELECTRICITY METERS ONLY.
 * Trilingual { hy, ru, en }.
 * ==========================================================================*/
window.DATA = window.DATA || {};

window.DATA.meters = {
  categories: [
    { id: "single", name: { hy: "Միաֆազ հաշվիչներ", ru: "Однофазные счётчики", en: "Single-phase meters" } },
    { id: "three",  name: { hy: "Եռաֆազ հաշվիչներ", ru: "Трёхфазные счётчики", en: "Three-phase meters" } },
    { id: "hv",     name: { hy: "Բարձրավոլտ հաշվառման սարքեր", ru: "Высоковольтные приборы учёта", en: "High-voltage metering devices" } }
  ],

  products: [
    {
      id: "mirtek-12-d17",
      category: "single",
      image: "assets/img/meters/mirtek-12-d17.png",
      name: "МИРТЕК-12-РУ-D17",
      form: { hy: "DIN-ռելս", ru: "DIN-рейка", en: "DIN-rail" },
      tagline: {
        hy: "Միաֆազ բազմասակագին խելացի հաշվիչ DIN-ռելսի վրա՝ ինտեգրված բեռի կառավարման ռելեով։",
        ru: "Однофазный многотарифный интеллектуальный счётчик на DIN-рейку со встроенным реле управления нагрузкой.",
        en: "Single-phase multi-tariff smart meter for DIN-rail with a built-in load-control relay."
      },
      accuracy: "1 / 1",
      current: "5 (80) A",
      interfaces: ["Optical", "RS-485", "RF 433", "GSM 2G/4G/LTE", "NB-IoT"],
      specs: [
        { label: { hy: "Ճշտության դաս (ակտիվ/ռեակտիվ)", ru: "Класс точности (акт./реакт.)", en: "Accuracy class (active/reactive)" }, value: "1 / 1" },
        { label: { hy: "Անվանական լարում", ru: "Номинальное напряжение", en: "Nominal voltage" }, value: "220 / 230 V" },
        { label: { hy: "Հոսանք (բազային/առավ.)", ru: "Ток (базовый/макс.)", en: "Current (base/max)" }, value: "5 (80) A" },
        { label: { hy: "Հաճախություն", ru: "Частота", en: "Frequency" }, value: "50 ± 7.5% Hz" },
        { label: { hy: "Ջերմաստիճանային միջակայք", ru: "Диапазон температур", en: "Temperature range" }, value: "−40…+70 °C" },
        { label: { hy: "Ստուգաչափման միջակայք", ru: "Межповерочный интервал", en: "Verification interval" }, value: { hy: "16 տարի", ru: "16 лет", en: "16 years" } },
        { label: { hy: "Ծառայության ժամկետ", ru: "Срок службы", en: "Service life" }, value: { hy: "≥48 տարի", ru: "≥48 лет", en: "≥48 years" } }
      ],
      features: [
        { hy: "Բազմասակագին հաշվառում, 128 օրական / 36 ամսական պրոֆիլ", ru: "Многотарифный учёт, 128 суточных / 36 месячных профилей", en: "Multi-tariff metering, 128 daily / 36 monthly profiles" },
        { hy: "Ինտեգրված բեռի կառավարման ռելե՝ ապարատային արգելափակմամբ", ru: "Встроенное реле управления нагрузкой с аппаратной блокировкой", en: "Built-in load-control relay with hardware blocking" },
        { hy: "Էլեկտրոնային կնիքներ և մագնիսական դաշտի տվիչ", ru: "Электронные пломбы и датчик магнитного поля", en: "Electronic seals and magnetic-field sensor" },
        { hy: "«Վերջին շունչ» ազդանշան GSM/NB-IoT-ով", ru: "«Последний вздох» по GSM/NB-IoT", en: "“Last gasp” power-fail notification via GSM/NB-IoT" }
      ]
    },
    {
      id: "mirtek-12-sp17",
      category: "single",
      image: "assets/img/meters/mirtek-12-sp17.png",
      name: "МИРТЕК-12-РУ-SP17",
      form: { hy: "Սփլիթ", ru: "Сплит", en: "Split" },
      tagline: {
        hy: "Սփլիթ-կառուցվածքի միաֆազ խելացի հաշվիչ՝ DLMS/COSEM և СПОДЭС աջակցությամբ, մինչև 100 Ա։",
        ru: "Однофазный сплит-счётчик с поддержкой DLMS/COSEM и СПОДЭС, до 100 А.",
        en: "Single-phase split-architecture smart meter supporting DLMS/COSEM and SPODES, up to 100 A."
      },
      accuracy: "1 / 1",
      current: "5 (100) A",
      interfaces: ["Optical", "RF 433/2400", "GSM 2G/4G/LTE", "NB-IoT"],
      specs: [
        { label: { hy: "Ճշտության դաս", ru: "Класс точности", en: "Accuracy class" }, value: "1 / 1" },
        { label: { hy: "Անվանական լարում", ru: "Номинальное напряжение", en: "Nominal voltage" }, value: "220 / 230 V" },
        { label: { hy: "Հոսանք (բազային/առավ.)", ru: "Ток (базовый/макс.)", en: "Current (base/max)" }, value: "5 (100) A" },
        { label: { hy: "Արձանագրություններ", ru: "Протоколы", en: "Protocols" }, value: "МИРТЕК, DLMS/COSEM, СПОДЭС v4" },
        { label: { hy: "Ջերմաստիճան", ru: "Температура", en: "Temperature" }, value: "−40…+70 °C (F: −45…+85)" },
        { label: { hy: "Ստուգաչափման միջակայք", ru: "Межповерочный интервал", en: "Verification interval" }, value: { hy: "16 տարի", ru: "16 лет", en: "16 years" } }
      ],
      features: [
        { hy: "DLMS/COSEM և СПОДЭС ГОСТ Р 58940-2020 համապատասխանություն", ru: "Соответствие DLMS/COSEM и СПОДЭС по ГОСТ Р 58940-2020", en: "DLMS/COSEM & SPODES compliant (GOST R 58940-2020)" },
        { hy: "Փոխարինելի կապի մոդուլներ (hot-swap)", ru: "Сменные модули связи (hot-swap)", en: "Interchangeable communication modules (hot-swap)" },
        { hy: "Մագնիսական դաշտի տվիչ և հակագողության պաշտպանություն", ru: "Датчик магнитного поля и антивандальная защита", en: "Magnetic-field sensor and anti-tamper protection" }
      ]
    },
    {
      id: "mirtek-12-w9",
      category: "single",
      image: "assets/img/meters/mirtek-12-w9.png",
      name: "МИРТЕК-12-РУ-W9",
      form: { hy: "Վահանակ", ru: "Щиток", en: "Panel" },
      tagline: {
        hy: "Վահանակային միաֆազ հաշվիչ՝ երկկողմ հաշվառմամբ և ստուգաչափողի կնիքը չխախտող մարտկոցի փոխարինմամբ։",
        ru: "Панельный однофазный счётчик с двунаправленным учётом и заменой батарейки без нарушения пломбы госповерителя.",
        en: "Panel-mount single-phase meter with bidirectional metering and battery replacement without breaking the verifier’s seal."
      },
      accuracy: "1 / 1",
      current: "5 (60/80) A",
      interfaces: ["Optical", "RS-485", "RF 433", "GSM", "NB-IoT"],
      specs: [
        { label: { hy: "Ճշտության դաս", ru: "Класс точности", en: "Accuracy class" }, value: "1 / 1" },
        { label: { hy: "Անվանական լարում", ru: "Номинальное напряжение", en: "Nominal voltage" }, value: "220 / 230 V" },
        { label: { hy: "Հոսանք", ru: "Ток", en: "Current" }, value: "5 (60/80) A" },
        { label: { hy: "Ջերմաստիճան", ru: "Температура", en: "Temperature" }, value: "−40…+70 °C" },
        { label: { hy: "Ծառայության ժամկետ", ru: "Срок службы", en: "Service life" }, value: { hy: "≥35 տարի", ru: "≥35 лет", en: "≥35 years" } }
      ],
      features: [
        { hy: "Երկկողմ (ներմուծում/արտահանում) հաշվառման տարբերակ", ru: "Двунаправленный учёт (импорт/экспорт)", en: "Bidirectional (import/export) metering option" },
        { hy: "Երկակի SIM և մագնիսական տվիչ", ru: "Двойная SIM и магнитный датчик", en: "Dual SIM and magnetic sensor" }
      ]
    },
    {
      id: "mirtek-32-d37",
      category: "three",
      image: "assets/img/meters/mirtek-32-d37.png",
      name: "МИРТЕК-32-РУ-D37",
      form: { hy: "DIN-ռելս", ru: "DIN-рейка", en: "DIN-rail" },
      tagline: {
        hy: "Եռաֆազ բազմաֆունկցիոնալ հաշվիչ DIN-ռելսի վրա՝ գրաֆիկական ցուցասարքով և իրադարձությունների գրանցամատյանով։",
        ru: "Трёхфазный многофункциональный счётчик на DIN-рейку с графическим дисплеем и журналом событий.",
        en: "Three-phase multifunction DIN-rail meter with a graphical display and event log."
      },
      accuracy: "0.5S / 1",
      current: "5 (10/100) A",
      interfaces: ["Optical", "RS-485", "RF 433", "GSM/NB-IoT"],
      specs: [
        { label: { hy: "Ճշտության դաս", ru: "Класс точности", en: "Accuracy class" }, value: "0.5S / 1 · 1 / 1" },
        { label: { hy: "Լարում", ru: "Напряжение", en: "Voltage" }, value: "57.7 / 220 / 230 V" },
        { label: { hy: "Հոսանք (բազ./առավ.)", ru: "Ток (баз./макс.)", en: "Current (base/max)" }, value: "5 (10) / 5 (100) A" },
        { label: { hy: "Ջերմաստիճան", ru: "Температура", en: "Temperature" }, value: "−40…+70 °C" },
        { label: { hy: "Իրադարձությունների գրանցում", ru: "Журнал событий", en: "Event log" }, value: "≥500" },
        { label: { hy: "Ստուգաչափում", ru: "Поверка", en: "Verification" }, value: { hy: "10 / 16 տարի", ru: "10 / 16 лет", en: "10 / 16 years" } }
      ],
      features: [
        { hy: "Եռաֆազ բեռի ռելե՝ ապարատային արգելափակմամբ", ru: "Трёхфазное реле нагрузки с аппаратной блокировкой", en: "Three-phase load relay with hardware blocking" },
        { hy: "Ընտրովի դիսկրետ մուտք/ելք, արտաքին մարտկոց մինչև 16 տարի", ru: "Опциональные дискретные I/O, внешняя батарея до 16 лет", en: "Optional discrete I/O, external battery up to 16 years" }
      ]
    },
    {
      id: "mirtek-32-w32",
      category: "three",
      image: "assets/img/meters/mirtek-32-w32.png",
      name: "МИРТЕК-32-РУ-W32",
      form: { hy: "Վահանակ", ru: "Щиток", en: "Panel" },
      tagline: {
        hy: "Ամենաճշգրիտ եռաֆազ հաշվիչ (մինչև 0.2S)՝ ուղիղ և տրանսֆորմատորային միացմամբ, Ethernet-ով։",
        ru: "Самый точный трёхфазный счётчик (до 0.2S) прямого и трансформаторного включения, с Ethernet.",
        en: "The most accurate three-phase meter (up to 0.2S) for direct and transformer connection, with Ethernet."
      },
      accuracy: "0.2S / 1",
      current: "1/5/10 (10/100) A",
      interfaces: ["Optical", "RS-485", "Ethernet", "RF 433/2400", "GSM/NB-IoT"],
      specs: [
        { label: { hy: "Ճշտության դաս", ru: "Класс точности", en: "Accuracy class" }, value: "0.2S / 0.5S / 1" },
        { label: { hy: "Լարում", ru: "Напряжение", en: "Voltage" }, value: "57.7 / 220 / 230 V" },
        { label: { hy: "Հոսանք", ru: "Ток", en: "Current" }, value: "1 / 5 / 10 (10/100) A" },
        { label: { hy: "Միացում", ru: "Включение", en: "Connection" }, value: { hy: "Ուղիղ և տրանսֆորմատորային", ru: "Прямое и трансформаторное", en: "Direct and transformer" } },
        { label: { hy: "Ծառայության ժամկետ", ru: "Срок службы", en: "Service life" }, value: { hy: "≥35 տարի", ru: "≥35 лет", en: "≥35 years" } }
      ],
      features: [
        { hy: "Ethernet + երկակի SIM արդյունաբերական հաշվառման համար", ru: "Ethernet + двойная SIM для промышленного учёта", en: "Ethernet + dual SIM for industrial metering" },
        { hy: "Ուղիղ և տրանսֆորմատորային միացման ունիվերսալ սարք", ru: "Универсальный прибор прямого и трансформаторного включения", en: "Universal direct- and transformer-connection device" }
      ]
    },
    {
      id: "mirtek-32-sp31",
      category: "three",
      image: "assets/img/meters/mirtek-32-sp31.png",
      name: "МИРТЕК-32-РУ-SP31",
      form: { hy: "Սփլիթ", ru: "Сплит", en: "Split" },
      tagline: {
        hy: "Տրանսֆորմատորային միացման եռաֆազ սփլիթ-հաշվիչ՝ առանձին МИРТ-830 ցուցասարքով։",
        ru: "Трёхфазный сплит-счётчик трансформаторного включения с отдельным дисплеем МИРТ-830.",
        en: "Three-phase split meter for transformer connection with a separate MIRT-830 display module."
      },
      accuracy: "1 / 1",
      current: "5 (100) A",
      interfaces: ["Optical", "RF 433/868/2400", "GSM/LTE", "NB-IoT"],
      specs: [
        { label: { hy: "Ճշտության դաս", ru: "Класс точности", en: "Accuracy class" }, value: "1 / 1" },
        { label: { hy: "Լարում", ru: "Напряжение", en: "Voltage" }, value: "220 / 230 V" },
        { label: { hy: "Միացում", ru: "Включение", en: "Connection" }, value: { hy: "Տրանսֆորմատորային", ru: "Трансформаторное", en: "Transformer" } },
        { label: { hy: "Ցուցասարք", ru: "Дисплей", en: "Display" }, value: "МИРТ-830" },
        { label: { hy: "Ստուգաչափում", ru: "Поверка", en: "Verification" }, value: { hy: "16 տարի", ru: "16 лет", en: "16 years" } }
      ],
      features: [
        { hy: "Երկկողմ հաշվառում (D-տարբերակ)", ru: "Двунаправленный учёт (вариант D)", en: "Bidirectional metering (D variant)" },
        { hy: "МИРТЕК + СПОДЭС արձանագրություններ", ru: "Протоколы МИРТЕК + СПОДЭС", en: "MIRTEK + SPODES protocols" }
      ]
    },
    {
      id: "mirtek-135",
      category: "hv",
      image: "assets/img/meters/mirtek-135.png",
      name: "МИРТЕК-135-РУ",
      form: { hy: "6/10 կՎ", ru: "6/10 кВ", en: "6/10 kV" },
      tagline: {
        hy: "Միջին լարման (6/10 կՎ) հաշվառման սարք՝ Ռոգովսկու կոճով հոսանքի տվիչներով և GLONASS/GPS ժամանակի համաժամացմամբ։",
        ru: "Прибор учёта среднего напряжения (6/10 кВ) с датчиками тока на катушке Роговского и синхронизацией GLONASS/GPS.",
        en: "Medium-voltage (6/10 kV) metering device with Rogowski-coil current sensors and GLONASS/GPS time synchronization."
      },
      accuracy: "0.5S / 1",
      current: "5/10/20 (100/200/300) A",
      interfaces: ["RF 433", "GSM/GPRS", "Optical fiber", "GLONASS/GPS"],
      specs: [
        { label: { hy: "Ճշտության դաս (ակտ./ռեակտ.)", ru: "Класс точности (акт./реакт.)", en: "Accuracy class (active/reactive)" }, value: "0.5S / 1" },
        { label: { hy: "Անվանական լարում", ru: "Номинальное напряжение", en: "Nominal voltage" }, value: "6 kV / 10 kV" },
        { label: { hy: "Հոսանք (անվ./առավ.)", ru: "Ток (ном./макс.)", en: "Current (nom./max)" }, value: "5/10/20 (100/200/300) A" },
        { label: { hy: "Ջերմային կայունություն", ru: "Термическая стойкость", en: "Thermal withstand" }, value: "12.5 kA / 2 s" },
        { label: { hy: "Ջերմաստիճան", ru: "Температура", en: "Temperature" }, value: "−45…+70 °C" },
        { label: { hy: "Ծառայության ժամկետ", ru: "Срок службы", en: "Service life" }, value: { hy: "≥30 տարի", ru: "≥30 лет", en: "≥30 years" } }
      ],
      features: [
        { hy: "Ռոգովսկու կոճով էլեկտրոնային հոսանքի տվիչներ (առանց ՀՏ)", ru: "Электронные датчики тока на катушке Роговского (без ТТ)", en: "Rogowski-coil electronic current sensors (no CTs)" },
        { hy: "Օդային գծերի (ՕԳ/СИП) և ԿՌՈՒ/КСО խցիկների համար", ru: "Для воздушных линий (ВЛ/СИП) и ячеек КРУ/КСО", en: "For overhead lines (OHL/SIP) and KRU/KSO switchgear cells" },
        { hy: "GLONASS/GPS ժամանակի համաժամացում", ru: "Синхронизация времени GLONASS/GPS", en: "GLONASS/GPS time synchronization" }
      ]
    }
  ],

  /* Cross-cutting metering technology narrative -------------------------- */
  technology: [
    { icon: "wifi",   title: { hy: "Խելացի հաշվառում (AMR/AMI)", ru: "Умный учёт (AMR/AMI)", en: "Smart metering (AMR/AMI)" },
      text: { hy: "GSM, NB-IoT, RF 433/868/2400 ՄՀց, RS-485 և Ethernet հեռակառավարման ինտերֆեյսներ, երկակի SIM ավելցուկայնություն։", ru: "Интерфейсы удалённого доступа GSM, NB-IoT, RF 433/868/2400 МГц, RS-485 и Ethernet, резервирование двумя SIM.", en: "Remote-access interfaces GSM, NB-IoT, RF 433/868/2400 MHz, RS-485 and Ethernet, dual-SIM redundancy." } },
    { icon: "shield", title: { hy: "Հակագողության պաշտպանություն", ru: "Антивандальная защита", en: "Anti-tamper protection" },
      text: { hy: "Էլեկտրոնային կնիքներ, մագնիսական դաշտի տվիչ, բացման իրադարձությունների գրանցում (≥500)։", ru: "Электронные пломбы, датчик магнитного поля, журнал вскрытий (≥500 записей).", en: "Electronic seals, magnetic-field sensor, tamper/opening event log (≥500 records)." } },
    { icon: "code",   title: { hy: "Ստանդարտ արձանագրություններ", ru: "Стандартные протоколы", en: "Standard protocols" },
      text: { hy: "DLMS/COSEM և СПОДЭС (v2, 3.2, 4)՝ ГОСТ Р 58940-2020 համապատասխան։", ru: "DLMS/COSEM и СПОДЭС (v2, 3.2, 4) по ГОСТ Р 58940-2020.", en: "DLMS/COSEM and SPODES (v2, 3.2, 4) per GOST R 58940-2020." } },
    { icon: "clock",  title: { hy: "Երկարակեցություն", ru: "Долговечность", en: "Longevity" },
      text: { hy: "Ստուգաչափման միջակայք մինչև 16 տարի, ծառայության ժամկետ մինչև 48 տարի, MTBF ≥480 000 ժ։", ru: "Межповерочный интервал до 16 лет, срок службы до 48 лет, MTBF ≥480 000 ч.", en: "Verification interval up to 16 years, service life up to 48 years, MTBF ≥480,000 h." } }
  ],

  /* Documentation types (per product) ----------------------------------- */
  docTypes: [
    { hy: "Տիպի սերտիֆիկատ և նկարագրություն", ru: "Сертификат и описание типа", en: "Type-approval certificate & description" },
    { hy: "Համապատասխանության հայտարարագիր", ru: "Декларация о соответствии", en: "Declaration of conformity" },
    { hy: "Շահագործման ձեռնարկ", ru: "Руководство по эксплуатации", en: "Operating manual" },
    { hy: "Կապի մոդուլի ձեռնարկ", ru: "Руководство по модулю связи", en: "Communication-module manual" },
    { hy: "Ստուգաչափման մեթոդիկա", ru: "Методика поверки", en: "Verification methodology" },
    { hy: "Անտենայի/մոնտաժի հրահանգ", ru: "Инструкция по монтажу антенны", en: "Antenna/mounting instructions" }
  ]
};
