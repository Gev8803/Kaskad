# -*- coding: utf-8 -*-
"""
Migrate the existing hardcoded frontend content into the database.

Transcribes every record from the current source-of-truth files:
  site/assets/js/data.common.js
  site/assets/js/data.construction.js
  site/assets/js/data.switchgear.js
  site/assets/js/data.meters.js
  site/assets/js/i18n.js
  and the hardcoded `news` array in site/assets/js/app.js

Usage:
    py manage.py seed_content            # seeds only if content is empty
    py manage.py seed_content --force    # wipe content models and reseed

`--force` never touches users or contact messages.
"""
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from content import models as m


def tri(hy, ru, en):
    return {"hy": hy, "ru": ru, "en": en}


class Command(BaseCommand):
    help = "Seed the database with the existing frontend content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", action="store_true",
            help="Delete existing content and reseed from source.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options["force"]
        already = m.SwitchgearCategory.objects.exists() or m.Service.objects.exists()
        if already and not force:
            self.stdout.write(self.style.WARNING(
                "Content already present. Re-run with --force to wipe and reseed."
            ))
            return
        if force:
            self._wipe()

        self._site_settings()
        self._company()
        self._construction()
        self._switchgear()
        self._meters()
        self._news()
        self._ui_strings()

        self.stdout.write(self.style.SUCCESS("Content seeded successfully."))

    # ------------------------------------------------------------------ wipe
    def _wipe(self):
        for model in (
            m.ServicePoint, m.Service, m.Project, m.ProjectImage, m.ProjectCategory,
            m.SwitchgearItem, m.SwitchgearSpec, m.SwitchgearDoc, m.SwitchgearCategory,
            m.Certificate, m.MeterSpec, m.MeterFeature, m.Meter, m.MeterCategory,
            m.MeterTechnology, m.MeterDocType, m.Stat, m.Advantage, m.Value,
            m.Partner, m.Client, m.HistoryMilestone, m.News, m.GalleryImage,
            m.UIString,
        ):
            model.objects.all().delete()
        self.stdout.write("  Wiped existing content.")

    # -------------------------------------------------------------- settings
    def _site_settings(self):
        s = m.SiteSettings.load()
        s.address_hy = "Բագրատունյաց 54/3, Երևան, Հայաստան"
        s.address_ru = "Багратуняц 54/3, Ереван, Армения"
        s.address_en = "Bagratunyats 54/3, Yerevan, Armenia"
        s.phone = "+374 77 241 212"
        s.phone_link = "+37477241212"
        s.email = "info@kaskadgroup.am"
        s.map_embed = (
            "https://www.google.com/maps?q=Bagratunyats%2054%2F3%20"
            "Yerevan%20Armenia&output=embed"
        )
        s.manufacturing_hy = (
            "Արտադրությունն իրականացվում է Կալուգայի ժամանակակից գործարանում՝ "
            "Բելգիական DEBA ընկերության տեխնոլոգիայով։ Հավաքումն իրականացվում է "
            "հայրենական և ներմուծվող կոմպլեկտավորող տարրերից՝ բարձր ճշգրտության "
            "սարքավորումների վրա։ Ամբողջ արտադրանքը սերտիֆիկացված է և "
            "համապատասխանում է ГОСТ և IEC ստանդարտներին։"
        )
        s.manufacturing_ru = (
            "Производство осуществляется на современном заводе в г. Калуга по "
            "технологии бельгийской компании DEBA. Сборка ведётся из "
            "отечественных и импортных комплектующих на высокоточном "
            "оборудовании. Вся продукция сертифицирована и отвечает как "
            "российским (ГОСТ), так и международным (IEC) стандартам."
        )
        s.manufacturing_en = (
            "Manufacturing takes place at a modern plant in Kaluga using the "
            "technology of the Belgian company DEBA. Assembly uses domestic and "
            "imported components on high-precision equipment. All products are "
            "certified and comply with both Russian (GOST) and international "
            "(IEC) standards."
        )
        s.save()

    # --------------------------------------------------------------- company
    def _company(self):
        stats = [
            (20, "+", tri("տարվա փորձ", "лет опыта", "years of expertise")),
            (100, "+", tri("իրականացված նախագիծ", "реализованных проектов", "completed projects")),
            (5, "", tri("արտադրական հարթակ", "производственных площадок", "production sites")),
            (30, "+", tri("սպասարկվող տարածաշրջան", "обслуживаемых регионов", "regions served")),
        ]
        for i, (val, suf, lbl) in enumerate(stats):
            m.Stat.objects.create(
                value=val, suffix=suf, sort=i,
                label_hy=lbl["hy"], label_ru=lbl["ru"], label_en=lbl["en"],
            )

        advantages = [
            ("cycle", tri("Ամբողջական ցիկլ", "Полный цикл", "Full cycle"),
             tri("Նախագծումից մինչև օբյեկտի շահագործման հանձնում՝ մեկ պատասխանատու գործընկեր։",
                 "От проектирования до ввода объекта в эксплуатацию — один ответственный партнёр.",
                 "From design to commissioning — one accountable partner.")),
            ("factory", tri("Սեփական արտադրություն", "Собственное производство", "In-house manufacturing"),
             tri("Սեփական գործարաններ՝ միջին լարման բաշխիչ սարքերի, վահանակների և հաշվիչների արտադրության համար։",
                 "Собственные заводы для производства РУ среднего напряжения, щитов и счётчиков.",
                 "Own plants producing medium-voltage switchgear, boards and meters.")),
            ("medal", tri("Սերտիֆիկացված որակ", "Сертифицированное качество", "Certified quality"),
             tri("Արտադրանքը համապատասխանում է ГОСТ, IEC և ISO 9001 ստանդարտներին։",
                 "Продукция соответствует стандартам ГОСТ, IEC и ISO 9001.",
                 "Products comply with GOST, IEC and ISO 9001 standards.")),
            ("globe", tri("Միջազգային տեխնոլոգիաներ", "Международные технологии", "International technology"),
             tri("Բելգիական DEBA-ի տեխնոլոգիա և առաջատար եվրոպական բաղադրիչներ։",
                 "Технология бельгийской DEBA и ведущие европейские комплектующие.",
                 "Belgian DEBA technology and leading European components.")),
            ("team", tri("Փորձառու թիմ", "Опытная команда", "Experienced team"),
             tri("Ինժեներներ, նախագծողներ և մոնտաժային բրիգադներ՝ էներգետիկ օբյեկտների փորձով։",
                 "Инженеры, проектировщики и монтажные бригады с опытом на энергообъектах.",
                 "Engineers, designers and installation crews experienced on power facilities.")),
            ("shield", tri("Անվտանգություն և հուսալիություն", "Безопасность и надёжность", "Safety & reliability"),
             tri("Փոքր չափսեր, մոնտաժի հեշտություն, շահագործման հուսալիություն և էկոլոգիական անվտանգություն։",
                 "Малые габариты, простота монтажа, эксплуатационная надёжность и экологическая безопасность.",
                 "Compact footprint, easy installation, operational reliability and environmental safety.")),
        ]
        for i, (icon, title, text) in enumerate(advantages):
            m.Advantage.objects.create(
                icon=icon, sort=i,
                title_hy=title["hy"], title_ru=title["ru"], title_en=title["en"],
                text_hy=text["hy"], text_ru=text["ru"], text_en=text["en"],
            )

        partners = ["ABB", "Schneider Electric", "Legrand", "Hager",
                    "DEBA", "EKRA", "MIRTEK", "Elster Metronica"]
        for i, name in enumerate(partners):
            m.Partner.objects.create(name=name, sort=i)

        clients = [
            tri("Հայաստանի բարձրավոլտ էլեկտրացանցեր", "Высоковольтные электрические сети Армении", "High-Voltage Electric Networks of Armenia"),
            tri("Հայաստանի էլեկտրական ցանցեր", "Электрические сети Армении", "Electric Networks of Armenia"),
            tri("Ռուսատոմ Սերվիս (Ռոսատոմ)", "Русатом Сервис (Росатом)", "Rusatom Service (Rosatom)"),
            tri("Հայկական ԱԷԿ", "Армянская АЭС", "Armenian NPP"),
            tri("Интер РАО խումբ", "Группа Интер РАО", "Inter RAO Group"),
            tri("Россети", "ПАО Россети", "Rosseti PJSC"),
            tri("Մոսկվայի մետրոպոլիտեն", "Московский метрополитен", "Moscow Metro"),
            tri("Газпром", "Газпром", "Gazprom"),
        ]
        for i, name in enumerate(clients):
            m.Client.objects.create(
                sort=i, name_hy=name["hy"], name_ru=name["ru"], name_en=name["en"],
            )

        values = [
            ("bulb", tri("Նորարարություն", "Инновации", "Innovation"),
             tri("«Մենք նոր տեխնոլոգիաներ ենք ներդնում կյանք» — եվրոպական լուծումների կիրառում։",
                 "«Мы внедряем новые технологии в жизнь» — применение европейских решений.",
                 "“We bring new technologies to life” — applying European solutions.")),
            ("medal", tri("Որակ", "Качество", "Quality"),
             tri("Բարձր որակ, հուսալիություն և երկարակեցություն յուրաքանչյուր արտադրանքում։",
                 "Высокое качество, надёжность и долговечность в каждом изделии.",
                 "High quality, reliability and durability in every product.")),
            ("shield", tri("Անվտանգություն", "Безопасность", "Safety"),
             tri("Անձնակազմի և սարքավորումների անվտանգությունը՝ առաջնահերթություն։",
                 "Безопасность персонала и оборудования — приоритет.",
                 "Safety of personnel and equipment is a priority.")),
            ("leaf", tri("Էկոլոգիականություն", "Экологичность", "Sustainability"),
             tri("Էկոլոգիապես անվտանգ արտադրություն և արդյունավետ էներգիայի կառավարում։",
                 "Экологически безопасное производство и эффективное управление энергией.",
                 "Environmentally safe production and efficient energy management.")),
        ]
        for i, (icon, title, text) in enumerate(values):
            m.Value.objects.create(
                icon=icon, sort=i,
                title_hy=title["hy"], title_ru=title["ru"], title_en=title["en"],
                text_hy=text["hy"], text_ru=text["ru"], text_en=text["en"],
            )

        history = [
            ("2005", tri("«Կասկադ-Էներգո»-ի հիմնադրում՝ որպես «Կասկադ» հոլդինգի ինժեներա-շինարարական ուղղություն։",
                         "Основание «Каскад-Энерго» как инженерно-строительного направления холдинга «Каскад».",
                         "Kaskad-Energo founded as the engineering & construction arm of the Kaskad Holding.")),
            ("2010", tri("Կալուգայում ժամանակակից գործարանի գործարկում՝ Բելգիական DEBA-ի տեխնոլոգիայով միջին լարման սարքերի արտադրության համար։",
                         "Пуск современного завода в Калуге по технологии DEBA для производства РУ среднего напряжения.",
                         "Launch of a modern plant in Kaluga using DEBA technology for medium-voltage switchgear.")),
            ("2016", tri("Հայաստանում խոշոր ենթակայանների վերակառուցում՝ «Ախթանակ» 220 կՎ և «Փուրակ» 35/6 կՎ։",
                         "Реконструкция крупных подстанций в Армении: «Ахтанак» 220 кВ и «Пурак» 35/6 кВ.",
                         "Reconstruction of major substations in Armenia: Akhtanak 220 kV and Purak 35/6 kV.")),
            ("2019", tri("Խելացի հաշվառման զանգվածային ներդրում՝ Հայաստանում ~250 000 բաժանորդ, Ռուսաստանում 395 000+ հաշվառման կետ։",
                         "Массовое внедрение умного учёта: ~250 000 абонентов в Армении, 395 000+ точек учёта в России.",
                         "Large-scale smart-metering rollout: ~250,000 subscribers in Armenia, 395,000+ metering points in Russia.")),
            ("2026", tri("Երեք ուղղությունների միավորում մեկ խմբում՝ Երևանում կենտրոնակայանով։",
                         "Объединение трёх направлений в единую группу с головным офисом в Ереване.",
                         "Three divisions united into a single group headquartered in Yerevan.")),
        ]
        for i, (year, text) in enumerate(history):
            m.HistoryMilestone.objects.create(
                year=year, sort=i,
                text_hy=text["hy"], text_ru=text["ru"], text_en=text["en"],
            )

    # ---------------------------------------------------------- construction
    def _construction(self):
        services = [
            ("electrical", "bolt",
             tri("Էլեկտրամոնտաժային աշխատանքներ", "Электромонтажные работы", "Electrical Installation"),
             tri("Ցանկացած բարդության համալիր էլեկտրամոնտաժային աշխատանքներ արդյունաբերական, բնակելի, առևտրային և քաղաքային օբյեկտներում։",
                 "Комплексные электромонтажные работы любой сложности на промышленных, жилых, коммерческих и муниципальных объектах.",
                 "Comprehensive electrical installation of any complexity on industrial, residential, commercial and municipal facilities."),
             [tri("Էլեկտրամատակարարման համակարգեր (նախագծում, մատակարարում, մոնտաժ)", "Системы электроснабжения (проектирование, поставка, монтаж)", "Power supply systems (design, supply, installation)"),
              tri("Մալուխային գծերի անցկացում մինչև 110 կՎ և ավելի", "Прокладка кабельных линий до 110 кВ и выше", "Cable line laying up to 110 kV and above"),
              tri("Օդային էլեկտրահաղորդման գծեր (ՕԳ)", "Воздушные линии электропередачи (ВЛ)", "Overhead power lines (OHL)"),
              tri("Տրանսֆորմատորային ենթակայաններ մինչև 110 կՎ", "Трансформаторные подстанции до 110 кВ и выше", "Transformer substations up to 110 kV and above"),
              tri("Ռելեային պաշտպանության և ավտոմատիկայի համակարգեր (ՌՊԱ)", "Системы релейной защиты и автоматики (РЗА)", "Relay protection & automation (RPA)"),
              tri("Հողանցման և կայծակնապաշտպանության համակարգեր", "Системы заземления и молниезащита", "Earthing and lightning protection systems"),
              tri("Անխափան և պահուստային սնուցման համակարգեր (ԱՍ)", "Системы бесперебойного и резервного питания (ИБП)", "Uninterruptible & backup power (UPS)"),
              tri("Էլեկտրաէներգիայի հաշվառման համակարգեր (ԱՀՀՀ)", "Системы учёта электроэнергии (АСКУЭ)", "Electricity metering systems (AMR/AMI)")]),
            ("manufacturing", "factory",
             tri("Էներգետիկ սարքավորումների արտադրություն", "Производство энергетического оборудования", "Power Equipment Manufacturing"),
             tri("Ցածր լարման էլեկտրավահանակային սարքավորումների արտադրություն և հավաքում արդյունաբերական և քաղաքացիական շինարարության համար։",
                 "Производство и сборка низковольтного электрощитового оборудования для промышленного и гражданского строительства.",
                 "Manufacturing and assembly of low-voltage switchboard equipment for industrial and civil construction."),
             [tri("Կատալոգ՝ ավելի քան 50 տեսակի արտադրանք, 750 մոդիֆիկացիա", "Каталог: более 50 видов продукции, 750 модификаций", "Catalogue: 50+ product types, 750 modifications"),
              tri("Սեփական գործարան, ժամանակակից տեխնոլոգիաներ և սերտիֆիկացում", "Собственный завод, современные технологии и сертификация", "Own plant, modern technologies and certification"),
              tri("Կոմպլեկտավորում՝ ABB, Legrand, Schneider Electric, Hager", "Комплектующие: ABB, Legrand, Schneider Electric, Hager", "Components: ABB, Legrand, Schneider Electric, Hager")]),
            ("design-build", "blueprint",
             tri("Նախագծում և շինարարություն", "Проектирование и строительство", "Design & Construction"),
             tri("Նախագծման և շինարարության աշխատանքների ամբողջական համալիր՝ բնակելի, առևտրային, արդյունաբերական և ենթակառուցվածքային օբյեկտների համար։",
                 "Полный комплекс работ по проектированию и строительству жилых, коммерческих, промышленных и инфраструктурных объектов.",
                 "Full cycle of design and construction for residential, commercial, industrial and infrastructure facilities."),
             [tri("Բնակելի/առևտրային շենքեր, բիզնես և առևտրի կենտրոններ", "Жилые/коммерческие здания, бизнес- и торговые центры", "Residential/commercial buildings, business & retail centres"),
              tri("Էլեկտրական ենթակայաններ (ՏԵ, ՌՏԵ) 6–35 կՎ", "Электрические подстанции (ТП, РТП) 6–35 кВ", "Electrical substations (TS, DTS) 6–35 kV"),
              tri("Տրանսպորտային ենթակառուցվածք և քաղաքային էլեկտրատրանսպորտ", "Транспортная инфраструктура и городской электротранспорт", "Transport infrastructure and urban electric transport"),
              tri("ՇՌԿ անդամակցություն, «ՏԱՇԻՐ» շինարարական ընկերությունների միություն", "Членство в СРО, «Союз Строительных Компаний ТАШИР»", "SRO membership, TASHIR Construction Companies Union")]),
            ("acs", "network",
             tri("ԱՎՀ և հաշվառման համակարգեր", "Системы АСУ ТП и учёта", "SCADA & Metering Systems"),
             tri("«Կասկադ» հոլդինգի տեխնոլոգիական գործընթացների ավտոմատ կառավարման համակարգեր (ԱՎՀ) և էլեկտրաէներգիայի հաշվառում։",
                 "Автоматизированные системы управления технологическими процессами (АСУ ТП) и учёта электроэнергии Холдинга «Каскад».",
                 "Automated process-control (SCADA/DCS) and electricity-metering systems of the Kaskad Holding."),
             [tri("Նախանախագծային հետազոտություններ և ՏԱ մշակում", "Предпроектные обследования и разработка ТЗ", "Pre-design surveys and requirements development"),
              tri("Հաշվառման, կապի և սերվերային պահարանների մշակում", "Разработка шкафов учёта, связи и серверных шкафов", "Development of metering, communication and server cabinets"),
              tri("Ծրագրային հարթակներ՝ «Альфа Центр», «Пирамида 2.0», «Радиоэксесс»", "Платформы: «Альфа Центр», «Пирамида 2.0», «Радиоэксесс»", "Platforms: Alpha Center, Piramida 2.0, Radioexess"),
              tri("Բազմառեսուրս հաշվառում (գազ, ջուր, ջերմ) և թվային ենթակայան", "Многоресурсный учёт (газ, вода, тепло) и цифровая подстанция", "Multi-resource metering (gas, water, heat) and digital substation")]),
            ("commissioning", "gauge",
             tri("Գործարկման-կարգաբերման աշխատանքներ", "Пусконаладочные работы", "Commissioning Works"),
             tri("Էլեկտրասարքավորումների ստուգման, կարգաբերման և փորձարկման համալիր՝ նախագծային պարամետրերն ապահովելու համար։",
                 "Комплекс проверки, настройки и испытаний электрооборудования для обеспечения проектных параметров и режимов.",
                 "A set of checks, tuning and testing of electrical equipment to achieve design parameters and modes."),
             [tri("I փուլ՝ ԳԿԱ ծրագրի մշակում, չափման միջոցների նախապատրաստում", "I этап: разработка программы ПНР, подготовка средств измерений", "Stage I: commissioning programme, preparation of instruments"),
              tri("II փուլ՝ կառավարման վահանակների, պաշտպանության և ավտոմատիկայի կարգաբերում", "II этап: наладка панелей управления, защит и автоматики", "Stage II: tuning of control panels, protection and automation"),
              tri("III փուլ՝ սարքավորումների անհատական փորձարկումներ, արձանագրություններ", "III этап: индивидуальные испытания оборудования, протоколы", "Stage III: individual equipment tests and protocols"),
              tri("IV փուլ՝ համալիր փորձարկումներ պարապ և բեռնվածքի տակ", "IV этап: комплексные испытания на холостом ходу и под нагрузкой", "Stage IV: integrated tests at no-load and under load")]),
            ("testing", "test",
             tri("Էլեկտրական փորձարկումներ և չափումներ", "Электрические испытания и измерения", "Electrical Testing & Measurement"),
             tri("Մինչև և բարձր 1000 Վ էլեկտրասարքավորումների փորձարկումներ սեփական էլեկտրալաբորատորիայի և շարժական լաբորատորիայի միջոցով (գրանցում №245, №245/1)։",
                 "Испытания электрооборудования до и выше 1000 В собственной и передвижной электролабораторией (свидетельства №245, №245/1).",
                 "Testing of electrical equipment below and above 1000 V by our own and mobile electrical labs (registration No. 245, 245/1)."),
             [tri("Մեկուսացման և հողանցման դիմադրության չափում", "Измерение сопротивления изоляции и заземляющих устройств", "Insulation and earthing resistance measurement"),
              tri("Պաշտպանության գործարկման ստուգում (TN-C, TN-C-S, TN-S)", "Проверка срабатывания защиты (TN-C, TN-C-S, TN-S)", "Protection tripping verification (TN-C, TN-C-S, TN-S)"),
              tri("Ջերմատեսողական հետազոտություն և մասնակի պարպումների չափում", "Тепловизионное обследование и измерение частичных разрядов", "Thermal imaging and partial-discharge measurement"),
              tri("Շարժական լաբորատորիա (LVI HVT)՝ մալուխի վնասների տեղորոշում", "Передвижная лаборатория (LVI HVT): локализация повреждений кабеля", "Mobile lab (LVI HVT): cable-fault location")]),
        ]
        for i, (slug, icon, name, summary, points) in enumerate(services):
            svc = m.Service.objects.create(
                slug=slug, icon=icon, sort=i,
                name_hy=name["hy"], name_ru=name["ru"], name_en=name["en"],
                summary_hy=summary["hy"], summary_ru=summary["ru"], summary_en=summary["en"],
            )
            for j, p in enumerate(points):
                m.ServicePoint.objects.create(
                    service=svc, sort=j,
                    text_hy=p["hy"], text_ru=p["ru"], text_en=p["en"],
                )

        cats = [
            ("all", tri("Բոլորը", "Все", "All")),
            ("substation", tri("Ենթակայաններ", "Подстанции", "Substations")),
            ("generation", tri("Գեներացիա", "Генерация", "Generation")),
        ]
        for i, (slug, name) in enumerate(cats):
            m.ProjectCategory.objects.create(
                slug=slug, sort=i,
                name_hy=name["hy"], name_ru=name["ru"], name_en=name["en"],
            )

        projects = [
            ("zatonskaya", "ru", "2017", "generation", "440 MW · 290 Gcal/h",
             tri("Զատոնսկայա ՋԷԿ-ի կառուցում", "Строительство Затонской ТЭЦ", "Zatonskaya CHP Plant Construction"),
             tri("Ուֆա, Ռուսաստան", "Уфа, Россия", "Ufa, Russia"),
             tri("«Интер РАО» խումբ", "Группа «Интер РАО»", "Inter RAO Group"),
             tri("Ռուսաստանի ամենահզոր և ժամանակակից ջերմաէլեկտրակենտրոններից մեկը՝ 440 ՄՎտ էլեկտրական և 290 Գկալ/ժ ջերմային հզորությամբ։",
                 "Одна из самых мощных и современных теплоэлектроцентралей: 440 МВт электрической и 290 Гкал/ч тепловой мощности.",
                 "One of the most powerful and modern combined heat-and-power plants: 440 MW electrical and 290 Gcal/h thermal capacity.")),
            ("akhtanak", "am", "2016–2019", "substation", "220 kV · 125 MVA",
             tri("«Ախթանակ» ենթակայանի վերակառուցում", "Реконструкция ПС «Ахтанак»", "Akhtanak Substation Reconstruction"),
             tri("Հայաստան", "Армения", "Armenia"),
             tri("«Հայաստանի բարձրավոլտ էլեկտրացանցեր» ՓԲԸ", "ЗАО «Высоковольтные электрические сети Армении»", "High-Voltage Electric Networks of Armenia CJSC"),
             tri("220 կՎ բաշխիչ սարքի վերակառուցում, 220/110/10 կՎ 125 ՄՎԱ ավտոտրանսֆորմատորների, գծային-կարգավորիչ տրանսֆորմատորների և ռեակտորների մոնտաժ, պաշտպանության և ավտոմատիկայի համակարգեր։",
                 "Реконструкция РУ 220 кВ, монтаж автотрансформаторов 220/110/10 кВ 125 МВА, линейно-регулировочных трансформаторов, реакторов, систем защиты и автоматики.",
                 "Reconstruction of the 220 kV switchgear; installation of 220/110/10 kV 125 MVA autotransformers, line voltage regulators, reactors, and protection & automation systems.")),
            ("purak", "am", "2016–2019", "substation", "35/6 kV · 25 MVA",
             tri("«Փուրակ» ենթակայանի վերակառուցում", "Реконструкция ПС «Пурак»", "Purak Substation Reconstruction"),
             tri("Հայաստան", "Армения", "Armenia"),
             tri("«Հայաստանի էլեկտրական ցանցեր» ՓԲԸ", "ЗАО «Электрические сети Армении»", "Electric Networks of Armenia CJSC"),
             tri("35/6 կՎ բաշխիչ սարքի, պաշտպանության և ավտոմատիկայի համակարգերի վերակառուցում՝ 25 ՄՎԱ տրանսֆորմատորներով։",
                 "Реконструкция РУ 35/6 кВ, систем защиты и автоматики, трансформаторы 25 МВА.",
                 "Reconstruction of the 35/6 kV switchgear and protection & automation systems, with 25 MVA transformers.")),
            ("anpp", "am", "—", "generation", "110 & 220 kV OSG",
             tri("Հայկական ԱԷԿ ինժեներական հետազննություններ", "Инженерные изыскания на Армянской АЭС", "Armenian NPP Engineering Surveys"),
             tri("Հայաստան", "Армения", "Armenia"),
             tri("«Ռուսատոմ Սերվիս» (Ռոսատոմ), Հայկական ԱԷԿ", "АО «Русатом Сервис» ГК Росатом; ЗАО «Армянская АЭС»", "Rusatom Service JSC (Rosatom); Armenian NPP CJSC"),
             tri("110 կՎ և 220 կՎ բաց բաշխիչ սարքերի (ԲԲՍ) կառուցման նախագծանախահաշվային և աշխատանքային փաստաթղթերի մշակում։",
                 "Разработка проектно-сметной и рабочей документации на сооружение ОРУ 110 кВ и 220 кВ.",
                 "Development of design, estimate and working documentation for the construction of 110 kV and 220 kV open switchgear.")),
            ("echmiadzin", "am", "2017", "substation", "10 kV",
             tri("10 կՎ ՏԵ-ի կառուցում, Էջմիածին", "Строительство ТП 10 кВ, Эчмиадзин", "10 kV Substation Construction, Echmiadzin"),
             tri("Էջմիածին, Հայաստան", "г. Эчмиадзин, Армения", "Echmiadzin, Armenia"),
             tri("Հայ Առաքելական Սուրբ Եկեղեցի", "Святая Апостольская церковь", "Armenian Apostolic Church"),
             tri("10 կՎ տրանսֆորմատորային ենթակայանի կառուցում Մայր Աթոռ Սուրբ Էջմիածնի համալիրի համար։",
                 "Строительство трансформаторной подстанции 10 кВ для комплекса Святой Апостольской церкви.",
                 "Construction of a 10 kV transformer substation for the Mother See complex.")),
            ("circus", "am", "2017", "substation", "10 kV",
             tri("«Կրկես» 10 կՎ բաշխիչ կետ", "РП «Цирк» 10 кВ", "Circus 10 kV Distribution Point"),
             tri("Երևան, Հայաստան", "г. Ереван, Армения", "Yerevan, Armenia"),
             tri("—", "—", "—"),
             tri("10 կՎ բաշխիչ կետի (ԲԿ) կառուցում Երևան քաղաքում։",
                 "Строительство распределительного пункта (РП) 10 кВ в г. Ереван.",
                 "Construction of a 10 kV distribution point (DP) in Yerevan.")),
            ("sez-tomsk", "ru", "2013–2015", "substation", "110/35/10 kV",
             tri("«ՀՏԳ» ենթակայան", "ПС «ОЭЗ»", "SEZ Substation"),
             tri("Տոմսկ, Ռուսաստան", "г. Томск, Россия", "Tomsk, Russia"),
             tri("«Հատուկ տնտեսական գոտիներ» ԲԸ", "ОАО «Особые экономические зоны»", "Special Economic Zones OJSC"),
             tri("110/35/10 կՎ տրանսֆորմատորային ենթակայանի կառուցում Տոմսկի հատուկ տնտեսական գոտու համար։",
                 "Строительство трансформаторной подстанции 110/35/10 кВ для особой экономической зоны Томска.",
                 "Construction of a 110/35/10 kV transformer substation for the Tomsk special economic zone.")),
        ]
        for i, (slug, country, year, cat, spec, name, loc, client, desc) in enumerate(projects):
            m.Project.objects.create(
                slug=slug, country=country, year=year, category=cat, spec=spec, sort=i,
                name_hy=name["hy"], name_ru=name["ru"], name_en=name["en"],
                location_hy=loc["hy"], location_ru=loc["ru"], location_en=loc["en"],
                client_hy=client["hy"], client_ru=client["ru"], client_en=client["en"],
                description_hy=desc["hy"], description_ru=desc["ru"], description_en=desc["en"],
            )

    # ------------------------------------------------------------ switchgear
    def _switchgear(self):
        # (slug, voltage, current(tri|None), name, summary, description, items, specs, docs)
        S = self._switchgear_data()
        for i, c in enumerate(S):
            cur = c["current"]
            cat = m.SwitchgearCategory.objects.create(
                slug=c["slug"], voltage=c["voltage"] or "", sort=i,
                current_hy=cur["hy"] if cur else "",
                current_ru=cur["ru"] if cur else "",
                current_en=cur["en"] if cur else "",
                name_hy=c["name"]["hy"], name_ru=c["name"]["ru"], name_en=c["name"]["en"],
                summary_hy=c["summary"]["hy"], summary_ru=c["summary"]["ru"], summary_en=c["summary"]["en"],
                description_hy=c["description"]["hy"], description_ru=c["description"]["ru"], description_en=c["description"]["en"],
            )
            for j, it in enumerate(c.get("items", [])):
                m.SwitchgearItem.objects.create(
                    category=cat, code=it["code"], sort=j,
                    name_hy=it["name"]["hy"], name_ru=it["name"]["ru"], name_en=it["name"]["en"],
                )
            for j, sp in enumerate(c.get("specs", [])):
                val = sp["value"]
                if isinstance(val, dict):
                    m.SwitchgearSpec.objects.create(
                        category=cat, sort=j,
                        label_hy=sp["label"]["hy"], label_ru=sp["label"]["ru"], label_en=sp["label"]["en"],
                        value_hy=val["hy"], value_ru=val["ru"], value_en=val["en"],
                    )
                else:
                    m.SwitchgearSpec.objects.create(
                        category=cat, sort=j, value_plain=val,
                        label_hy=sp["label"]["hy"], label_ru=sp["label"]["ru"], label_en=sp["label"]["en"],
                    )
            for j, d in enumerate(c.get("docs", [])):
                m.SwitchgearDoc.objects.create(
                    category=cat, sort=j, href=d.get("href", "#"),
                    label_hy=d["label"]["hy"], label_ru=d["label"]["ru"], label_en=d["label"]["en"],
                )

        certs = [
            (tri("ISO", "ISO", "ISO")),
            (tri("ГАЗПРОМСЕРТ", "СЕРТИФИКАТ ГАЗПРОМСЕРТ", "GAZPROMCERT")),
            (tri("KDW համապատասխանության սերտիֆիկատ", "KDW — сертификат соответствия", "KDW conformity certificate")),
            (tri("KD-3 համապատասխանության հայտարարագիր", "Декларация о соответствии KD-3", "KD-3 declaration of conformity")),
            (tri("KSO-KTiS համապատասխանության հայտարարագիր", "Декларация о соответствии КСО-КТИС", "KSO-KTiS declaration of conformity")),
        ]
        for i, title in enumerate(certs):
            m.Certificate.objects.create(
                sort=i, title_hy=title["hy"], title_ru=title["ru"], title_en=title["en"],
            )

    def _switchgear_data(self):
        return [
            {
                "slug": "kd-2", "voltage": "6–24 kV",
                "current": tri("մինչև 1250 Ա", "до 1250 А", "up to 1250 A"),
                "name": tri("KD-2 մոդուլներ (ԿՌՈՒ)", "Модули KD-2 (КРУ)", "KD-2 Modules (Switchgear)"),
                "summary": tri(
                    "Ներքին տեղակայման փոքրածավալ մոդուլային ԿՌՈՒ միակողմ սպասարկմամբ՝ 6–24 կՎ լարման եռաֆազ 50 Հց հոսանքի ընդունման և բաշխման համար։",
                    "Малогабаритное модульное комплектное распределительное устройство (КРУ) внутренней установки одностороннего обслуживания для приёма и распределения электроэнергии переменного трёхфазного тока 50 Гц напряжением 6–24 кВ.",
                    "Compact modular indoor switchgear (single-side maintenance) for receiving and distributing 3-phase 50 Hz power at 6–24 kV."),
                "description": tri(
                    "KD-2 մոդուլային կառուցվածքը միավորում է միջին լարման համակարգերի բոլոր գործառույթները։ Կիրառվում է քաղաքային և արդյունաբերական ցանցերի բաշխիչ կետերում ու տրանսֆորմատորային ենթակայաններում, գյուղատնտեսության և երկաթուղային տրանսպորտի էլեկտրաֆիկացման համար։",
                    "Модульная конструкция KD-2 объединила все функции систем среднего напряжения. Применяется в распределительных пунктах и трансформаторных подстанциях городских и промышленных сетей, для электрификации объектов сельского хозяйства и железнодорожного транспорта. Конструкция представляет собой набор различных по назначению ячеек по принципу «модульных блоков».",
                    "The KD-2 modular design unites all medium-voltage system functions. Used in distribution points and transformer substations of urban and industrial grids, and for electrification of agricultural and railway facilities. Built as a set of purpose-specific cells on a “modular block” principle."),
                "items": [
                    {"code": "KD-A", "name": tri("KD-A մոդուլ", "Модуль KD-A", "KD-A cell")},
                    {"code": "KD-AADt", "name": tri("KD-AADt մոդուլ", "Модуль KD-AADt", "KD-AADt cell")},
                    {"code": "KD-Ac", "name": tri("KD-Ac մոդուլ", "Модуль KD-Ac", "KD-Ac cell")},
                    {"code": "KD-AM", "name": tri("KD-AM մոդուլ", "Модуль KD-AM", "KD-AM cell")},
                    {"code": "KD-AV", "name": tri("KD-AV մոդուլ", "Модуль KD-AV", "KD-AV cell")},
                    {"code": "KD-C", "name": tri("KD-C մոդուլ", "Модуль KD-С", "KD-C cell")},
                    {"code": "KD-D", "name": tri("KD-D մոդուլ", "Модуль KD-D", "KD-D cell")},
                    {"code": "KD-D-500", "name": tri("KD-D-500 մոդուլ", "Модуль KD-D-500", "KD-D-500 cell")},
                    {"code": "KD-DT", "name": tri("KD-DT մոդուլ", "Модуль KD-DT", "KD-DT cell")},
                    {"code": "KD-LK", "name": tri("KD-LK մոդուլ", "Модуль KD-LK", "KD-LK cell")},
                    {"code": "KD-LKB", "name": tri("KD-LKB մոդուլ", "Модуль KD-LKB", "KD-LKB cell")},
                    {"code": "KD-P", "name": tri("KD-P մոդուլ", "Модуль KD-P", "KD-P cell")},
                    {"code": "KD-SN", "name": tri("KD-SN մոդուլ", "Модуль KD-SN", "KD-SN cell")},
                    {"code": "KD-T", "name": tri("KD-T մոդուլ", "Модуль KD-T", "KD-T cell")},
                    {"code": "KD-Z", "name": tri("KD-Z մոդուլ", "Модуль KD-Z", "KD-Z cell")},
                    {"code": "KD-K", "name": tri("KD-K մոդուլ", "Модуль KD-K", "KD-K cell")},
                ],
                "specs": [
                    {"label": tri("Անվանական լարում", "Номинальное напряжение", "Rated voltage"), "value": "6 / 10 / 24 kV"},
                    {"label": tri("Անվանական հոսանք", "Номинальный ток", "Rated current"), "value": tri("մինչև 1250 Ա", "до 1250 А", "up to 1250 A")},
                    {"label": tri("Հաճախություն", "Частота", "Frequency"), "value": "50 Hz"},
                ],
            },
            {
                "slug": "kdw", "voltage": "6–20 kV",
                "current": tri("630–3150 Ա", "630–3150 А", "630–3150 A"),
                "name": tri("KDW մոդուլներ (ԿՌՈՒ)", "Модули KDW (КРУ)", "KDW Modules (Withdrawable Switchgear)"),
                "summary": tri(
                    "Ներքին տեղակայման կասետային տիպի ԿՌՈՒ՝ 6–10 կՎ, 630–3150 Ա, մեկուսացված կամ փոխհատուցված չեզոքով ցանցերի համար։",
                    "Комплектные распределительные устройства (КРУ) внутренней установки кассетного типа для приёма и распределения электроэнергии 6–10 кВ, 630–3150 А в сетях с изолированной или компенсированной нейтралью.",
                    "Withdrawable-type indoor switchgear (cassette design) for 6–10 kV, 630–3150 A networks with isolated or compensated neutral."),
                "description": tri(
                    "KDW ԿՌՈՒ-ն բաղկացած է առանձին պահարաններից՝ կոմուտացիոն ապարատներով, չափիչ սարքերով, ավտոմատիկայի և պաշտպանության սարքերով։ Պահարանները պատրաստվում են բարձրորակ ցինկապատ պողպատից, արտաքին տարրերը՝ փոշեներկապատ։ Կիրառվող վակուումային անջատիչներ՝ BB/TEL, VD-4, ND-4, EVOLIS, LF։",
                    "КРУ серии KDW состоит из отдельных шкафов с коммутационными аппаратами, приборами измерения, устройствами автоматики и защиты. Шкафы изготовлены из высококачественной оцинкованной стали, наружные элементы окрашены методом порошкового напыления. Применяемые вакуумные выключатели — BB/TEL, VD-4, ND-4, EVOLIS, LF. Управление: местное, дистанционное и телемеханическое.",
                    "The KDW switchgear consists of separate cabinets with switching devices, metering instruments, automation and protection. Cabinets are made of high-grade galvanized steel with powder-coated outer elements. Vacuum circuit breakers used: BB/TEL, VD-4, ND-4, EVOLIS, LF. Control: local, remote and telemechanical."),
                "docs": [
                    {"label": tri("KDW նկարագրության PDF կատալոգ", "PDF каталог описания модуля KDW", "KDW description PDF catalogue"), "href": "#"},
                    {"label": tri("KDW բնութագրերի PDF կատալոգ", "PDF каталог характеристик KDW", "KDW specifications PDF catalogue"), "href": "#"},
                ],
                "specs": [
                    {"label": tri("Անվանական լարում (գծային)", "Номинальное напряжение (линейное)", "Rated voltage (line)"), "value": "6, 10, 20 kV"},
                    {"label": tri("Առավելագույն աշխ. լարում", "Наибольшее рабочее напряжение", "Max working voltage"), "value": "7.2; 12; 24 kV"},
                    {"label": tri("Գլխ. շղթաների անվ. հոսանք", "Номинальный ток главных цепей", "Rated main-circuit current"), "value": "630–3150 A"},
                    {"label": tri("Հավաքովի անվ. հոսանք", "Ток сборных шин", "Busbar rated current"), "value": "1600–3150 A"},
                    {"label": tri("Անջատման հոսանք", "Ток отключения выключателя", "Breaking current"), "value": "20; 25; 31.5 kA"},
                    {"label": tri("Ջերմային կայունություն (3վ)", "Ток термической стойкости (3 с)", "Thermal withstand (3 s)"), "value": "20; 25; 31.5 kA"},
                    {"label": tri("Էլեկտրադինամիկ կայունություն", "Электродинамическая стойкость", "Electrodynamic withstand"), "value": "51, 64, 81 kA"},
                    {"label": tri("Պաշտպանության աստիճան", "Степень защиты", "Protection degree"), "value": "IP 4X"},
                    {"label": tri("Կլիմայական կատարում", "Климатическое исполнение (ГОСТ 15150-69)", "Climatic version (GOST 15150-69)"), "value": "У3 (-45…+40 °C)"},
                    {"label": tri("Չափսեր L×B×H", "Габариты L×B×H, мм", "Dimensions L×W×H, mm"), "value": "750×1750×2330"},
                    {"label": tri("Զանգված", "Масса, не более", "Weight, max"), "value": "1000 kg"},
                    {"label": tri("Ծառայության ժամկետ", "Срок службы", "Service life"), "value": tri("30 տարի", "30 лет", "30 years")},
                ],
            },
            {
                "slug": "kso-ktis", "voltage": "6–10 kV",
                "current": tri("1000 Ա", "1000 А", "1000 A"),
                "name": tri("KSO/KTiS մոդուլներ", "Модули КСО - КТИС", "KSO/KTiS Chambers"),
                "summary": tri(
                    "Միակողմ սպասարկման հավաքովի խցիկներ (KSO/KTiS)՝ մինչև 10 կՎ, 50 Հց եռաֆազ հոսանքի ընդունման և բաշխման համար։",
                    "Камеры сборные одностороннего обслуживания серии КСО/КТиС для приёма и распределения электроэнергии трёхфазного переменного тока 50 Гц напряжением до 10 кВ.",
                    "Single-side maintenance assembled chambers (KSO/KTiS) for receiving and distributing 3-phase 50 Hz power up to 10 kV."),
                "description": tri(
                    "KSO/KTiS խցիկները նախատեսված են էլեկտրական ենթակայանների համալրման համար՝ մեկուսացված կամ փոխհատուցված չեզոքով ցանցերում։ Ամուր կմախքային մետաղական կառուցվածք՝ առջևի դռնով և կողային պատով, դիտման պատուհաններով։",
                    "Камеры КСО/КТиС предназначены для комплектования электрических подстанций в сетях с изолированной или компенсированной нейтралью. Представляют собой жёсткую каркасную металлическую конструкцию с передней дверью и боковой стенкой, с окнами для визуального наблюдения.",
                    "KSO/KTiS chambers are designed to equip electrical substations in networks with isolated or compensated neutral. A rigid frame metal structure with a front door and side wall, fitted with inspection windows."),
                "docs": [
                    {"label": tri("KSO/KTiS PDF կատալոգ", "PDF каталог модулей КСО-КТИС", "KSO/KTiS PDF catalogue"), "href": "#"},
                ],
                "specs": [
                    {"label": tri("Անվանական լարում", "Номинальное напряжение", "Rated voltage"), "value": "6; 10 kV"},
                    {"label": tri("Առավելագույն աշխ. լարում", "Наибольшее рабочее напряжение", "Max working voltage"), "value": "7.2; 12 kV"},
                    {"label": tri("Գլխ. շղթաների հոսանք", "Ток главных цепей", "Main-circuit current"), "value": "1000 A"},
                    {"label": tri("Հավաքովի շինաների հոսանք", "Ток сборных шин", "Busbar current"), "value": "1600–3150 A"},
                    {"label": tri("Անջատման հոսանք", "Ток отключения", "Breaking current"), "value": "12.5; 20 kA"},
                    {"label": tri("Պաշտպանության աստիճան", "Степень защиты", "Protection degree"), "value": "IP20, IP21"},
                    {"label": tri("Չափսեր", "Габариты, мм", "Dimensions, mm"), "value": "800×940×2450"},
                    {"label": tri("Զանգված", "Масса, не более", "Weight, max"), "value": "380 kg"},
                    {"label": tri("Ծառայության ժամկետ", "Срок службы", "Service life"), "value": tri("30 տարի", "30 лет", "30 years")},
                ],
            },
            {
                "slug": "kd-3", "voltage": "SF6 · до 24 kV",
                "current": tri("630 Ա", "630 А", "630 A"),
                "name": tri("KD-3 մոդուլներ (SF6)", "Модули KD-3 (элегаз SF6)", "KD-3 Modules (SF6)"),
                "summary": tri(
                    "Միջին լարման էլեգազային (SF6) մեկուսացմամբ միակողմ սպասարկման հավաքովի խցիկներ՝ կոմպակտ, սահմանափակ տարածքի օբյեկտների համար։",
                    "Камеры сборные одностороннего обслуживания серии KD-3 с элегазовой (SF6) изоляцией — компактные, для объектов с ограниченной площадью.",
                    "KD-3 single-side maintenance chambers with SF6 gas insulation — compact, for space-constrained facilities."),
                "description": tri(
                    "KD-3-ը մոդուլային բլոկային կառուցվածք է՝ SF6 գազով մեկուսացմամբ։ RV53 եռադիրք բեռի անջատիչը՝ ներկառուցված հողանցման անջատիչով, հերմետիկացված է ողջ ծառայության ընթացքում։ Համապատասխանում է ГОСТ և IEC 62271-200 ստանդարտներին։ KD3+ տարբերակը ներառում է SV-53 ներքին աղեղի մարիչ (<50 մվ)։",
                    "KD-3 — модульная конструкция на блочном принципе с изоляцией газом SF6. Трёхпозиционный выключатель нагрузки RV53 со встроенным заземлителем герметизирован на весь срок службы. Соответствует ГОСТ и IEC 62271-200. Вариант KD3+ включает гаситель внутренней дуги SV-53 (<50 мс).",
                    "KD-3 is a block-principle modular design with SF6 gas insulation. The RV53 three-position load-break switch with built-in earthing switch is sealed for life. Compliant with GOST and IEC 62271-200. The KD3+ variant includes the SV-53 internal-arc quencher (<50 ms)."),
                "items": [
                    {"code": "KD3-A", "name": tri("Ներածող/ելանցող մալուխի խցիկ", "Ячейка с выключателем нагрузки RV53", "Load-break cell (RV53)")},
                    {"code": "KD3-A+", "name": tri("Աղեղնամարիչով խցիկ", "Ячейка с гасителем внутренней дуги", "Cell with internal-arc quencher")},
                    {"code": "KD3-P", "name": tri("Ապահովիչներով խցիկ", "Ячейка с плавкими предохранителями", "Fuse-protection cell")},
                    {"code": "KD3-D", "name": tri("Վակուումային անջատիչով խցիկ", "Ячейка с вакуумным выключателем", "Vacuum-breaker cell")},
                    {"code": "KD3-C", "name": tri("Չափիչ խցիկ", "Ячейка измерительная", "Metering cell")},
                    {"code": "KD3-K", "name": tri("Ներածման խցիկ", "Ячейка ввода", "Incoming cell")},
                ],
                "specs": [
                    {"label": tri("Մեկուսացում", "Изоляция", "Insulation"), "value": "SF6"},
                    {"label": tri("Բեռի անջատիչ", "Выключатель нагрузки", "Load-break switch"), "value": "RV53 / RV44"},
                    {"label": tri("Ստանդարտներ", "Стандарты", "Standards"), "value": "ГОСТ, IEC 62271-200"},
                ],
            },
            {
                "slug": "bktp", "voltage": "20/0.4 kV", "current": None,
                "name": tri("ԲԿՏԵ (BKTP)", "БКТП", "BKTP (Prefab Substation)"),
                "summary": tri(
                    "Բլոկային կոմպլեկտ տրանսֆորմատորային ենթակայաններ (ԲԿՏԵ)՝ 20/0.4 կՎ։",
                    "Блочные комплектные трансформаторные подстанции (БКТП) 20/0,4 кВ.",
                    "Prefabricated block transformer substations (BKTP) 20/0.4 kV."),
                "description": tri(
                    "ԲԿՏԵ-ն ամբողջական գործարանային պատրաստվածության ենթակայան է՝ միջին լարումը ցածր լարման փոխակերպելու համար։",
                    "БКТП — трансформаторная подстанция полной заводской готовности для преобразования среднего напряжения в низкое.",
                    "BKTP is a fully factory-assembled transformer substation converting medium voltage to low voltage."),
                "items": [
                    {"code": "BKTP-20/0.4", "name": tri("ԲԿՏԵ-20/0.4 կՎԱ", "БКТП-20/0,4 кВА", "BKTP-20/0.4 kVA")},
                ],
                "specs": [
                    {"label": tri("Լարում", "Напряжение", "Voltage"), "value": "20 / 0.4 kV"},
                ],
            },
            {
                "slug": "privody", "voltage": None, "current": None,
                "name": tri("Մեխանիկական շարժաբերներ", "Механические приводы", "Mechanical Drives"),
                "summary": tri(
                    "Բեռի անջատիչների և հողանցման անջատիչների մեխանիկական շարժաբերներ։",
                    "Механические приводы для выключателей нагрузки и заземлителей.",
                    "Mechanical drives for load-break switches and earthing switches."),
                "description": tri(
                    "DA և DP շարժաբերների շարք՝ միակի և կրկնակի գործառույթով, հարմարեցված KD-A, KD-P, KD-D, KD-K, KD-LK մոդուլներին։",
                    "Линейка приводов DA и DP с одинарной и двойной функцией, совместимых с модулями KD-A, KD-P, KD-D, KD-K, KD-LK.",
                    "DA and DP drive range, single- and dual-function, compatible with KD-A, KD-P, KD-D, KD-K, KD-LK modules."),
                "items": [
                    {"code": "DA-MEC", "name": tri("DA-MEC — կրկնակի գործառույթի շարժաբեր", "DA-MEC — механический привод с двойной функцией", "DA-MEC — dual-function drive")},
                    {"code": "DA-M-MEC", "name": tri("DA-M-MEC — կրկնակի գործառույթի շարժաբեր", "DA-M-MEC — привод с двойной функцией", "DA-M-MEC — dual-function drive")},
                    {"code": "DA-K-MEC", "name": tri("DA-K-MEC — միակի գործառույթի շարժաբեր", "DA-K-MEC — привод с одинарной функцией", "DA-K-MEC — single-function drive")},
                ],
                "specs": [],
            },
            {
                "slug": "components", "voltage": None, "current": None,
                "name": tri("Կոմպլեկտավորող տարրեր", "Комплектующие", "Components"),
                "summary": tri(
                    "Վակուումային անջատիչներ, բեռի անջատիչներ, հողանցման անջատիչներ և պաշտպանության ռելեներ։",
                    "Вакуумные выключатели, выключатели нагрузки, заземлители и реле защиты.",
                    "Vacuum circuit breakers, load-break switches, earthing switches and protection relays."),
                "description": tri(
                    "Մեխանիկական շարժաբերով վակուումային անջատիչներ՝ բաշխիչ սարքերի, տրանսֆորմատորների, գեներատորների և էլեկտրաշարժիչների կոմուտացիայի ու պաշտպանության համար։",
                    "Вакуумные выключатели с механическим приводом для коммутации и защиты распределительных устройств, трансформаторов, генераторов и электродвигателей.",
                    "Vacuum circuit breakers with mechanical drive for switching and protecting switchgear, transformers, generators and motors."),
                "items": [
                    {"code": "RV44", "name": tri("RV44 բեռի անջատիչ", "Выключатель нагрузки RV44", "RV44 load-break switch")},
                    {"code": "VA-2", "name": tri("VA-2 վակուումային անջատիչ", "Вакуумный выключатель VA-2", "VA-2 vacuum circuit breaker")},
                    {"code": "EM20", "name": tri("EM20 հողանցման անջատիչ", "Заземляющий выключатель ЕМ20", "EM20 earthing switch")},
                    {"code": "BB/TEL", "name": tri("BB/TEL եռաֆազ վակուումային անջատիչ", "Выключатель вакуумный трёхфазный ВВ/TEL", "BB/TEL three-phase vacuum breaker")},
                    {"code": "RP-600", "name": tri("RP-600 պաշտպանության ռելե", "Реле защиты RP-600", "RP-600 protection relay")},
                ],
                "specs": [],
            },
        ]

    # ---------------------------------------------------------------- meters
    def _meters(self):
        cats = [
            ("single", tri("Միաֆազ հաշվիչներ", "Однофазные счётчики", "Single-phase meters")),
            ("three", tri("Եռաֆազ հաշվիչներ", "Трёхфазные счётчики", "Three-phase meters")),
            ("hv", tri("Բարձրավոլտ հաշվառման սարքեր", "Высоковольтные приборы учёта", "High-voltage metering devices")),
        ]
        cat_objs = {}
        for i, (slug, name) in enumerate(cats):
            cat_objs[slug] = m.MeterCategory.objects.create(
                slug=slug, sort=i,
                name_hy=name["hy"], name_ru=name["ru"], name_en=name["en"],
            )

        for i, p in enumerate(self._meters_data()):
            meter = m.Meter.objects.create(
                slug=p["slug"], category=cat_objs[p["category"]], sort=i,
                name=p["name"], accuracy=p["accuracy"], current=p["current"],
                interfaces="\n".join(p["interfaces"]),
                form_hy=p["form"]["hy"], form_ru=p["form"]["ru"], form_en=p["form"]["en"],
                tagline_hy=p["tagline"]["hy"], tagline_ru=p["tagline"]["ru"], tagline_en=p["tagline"]["en"],
            )
            for j, sp in enumerate(p["specs"]):
                val = sp["value"]
                if isinstance(val, dict):
                    m.MeterSpec.objects.create(
                        meter=meter, sort=j,
                        label_hy=sp["label"]["hy"], label_ru=sp["label"]["ru"], label_en=sp["label"]["en"],
                        value_hy=val["hy"], value_ru=val["ru"], value_en=val["en"],
                    )
                else:
                    m.MeterSpec.objects.create(
                        meter=meter, sort=j, value_plain=val,
                        label_hy=sp["label"]["hy"], label_ru=sp["label"]["ru"], label_en=sp["label"]["en"],
                    )
            for j, f in enumerate(p["features"]):
                m.MeterFeature.objects.create(
                    meter=meter, sort=j,
                    text_hy=f["hy"], text_ru=f["ru"], text_en=f["en"],
                )

        tech = [
            ("wifi", tri("Խելացի հաշվառում (AMR/AMI)", "Умный учёт (AMR/AMI)", "Smart metering (AMR/AMI)"),
             tri("GSM, NB-IoT, RF 433/868/2400 ՄՀց, RS-485 և Ethernet հեռակառավարման ինտերֆեյսներ, երկակի SIM ավելցուկայնություն։",
                 "Интерфейсы удалённого доступа GSM, NB-IoT, RF 433/868/2400 МГц, RS-485 и Ethernet, резервирование двумя SIM.",
                 "Remote-access interfaces GSM, NB-IoT, RF 433/868/2400 MHz, RS-485 and Ethernet, dual-SIM redundancy.")),
            ("shield", tri("Հակագողության պաշտպանություն", "Антивандальная защита", "Anti-tamper protection"),
             tri("Էլեկտրոնային կնիքներ, մագնիսական դաշտի տվիչ, բացման իրադարձությունների գրանցում (≥500)։",
                 "Электронные пломбы, датчик магнитного поля, журнал вскрытий (≥500 записей).",
                 "Electronic seals, magnetic-field sensor, tamper/opening event log (≥500 records).")),
            ("code", tri("Ստանդարտ արձանագրություններ", "Стандартные протоколы", "Standard protocols"),
             tri("DLMS/COSEM և СПОДЭС (v2, 3.2, 4)՝ ГОСТ Р 58940-2020 համապատասխան։",
                 "DLMS/COSEM и СПОДЭС (v2, 3.2, 4) по ГОСТ Р 58940-2020.",
                 "DLMS/COSEM and SPODES (v2, 3.2, 4) per GOST R 58940-2020.")),
            ("clock", tri("Երկարակեցություն", "Долговечность", "Longevity"),
             tri("Ստուգաչափման միջակայք մինչև 16 տարի, ծառայության ժամկետ մինչև 48 տարի, MTBF ≥480 000 ժ։",
                 "Межповерочный интервал до 16 лет, срок службы до 48 лет, MTBF ≥480 000 ч.",
                 "Verification interval up to 16 years, service life up to 48 years, MTBF ≥480,000 h.")),
        ]
        for i, (icon, title, text) in enumerate(tech):
            m.MeterTechnology.objects.create(
                icon=icon, sort=i,
                title_hy=title["hy"], title_ru=title["ru"], title_en=title["en"],
                text_hy=text["hy"], text_ru=text["ru"], text_en=text["en"],
            )

        doc_types = [
            tri("Տիպի սերտիֆիկատ և նկարագրություն", "Сертификат и описание типа", "Type-approval certificate & description"),
            tri("Համապատասխանության հայտարարագիր", "Декларация о соответствии", "Declaration of conformity"),
            tri("Շահագործման ձեռնարկ", "Руководство по эксплуатации", "Operating manual"),
            tri("Կապի մոդուլի ձեռնարկ", "Руководство по модулю связи", "Communication-module manual"),
            tri("Ստուգաչափման մեթոդիկա", "Методика поверки", "Verification methodology"),
            tri("Անտենայի/մոնտաժի հրահանգ", "Инструкция по монтажу антенны", "Antenna/mounting instructions"),
        ]
        for i, d in enumerate(doc_types):
            m.MeterDocType.objects.create(
                sort=i, label_hy=d["hy"], label_ru=d["ru"], label_en=d["en"],
            )

    def _meters_data(self):
        return [
            {"slug": "mirtek-12-d17", "category": "single", "name": "МИРТЕК-12-РУ-D17",
             "form": tri("DIN-ռելս", "DIN-рейка", "DIN-rail"),
             "tagline": tri("Միաֆազ բազմասակագին խելացի հաշվիչ DIN-ռելսի վրա՝ ինտեգրված բեռի կառավարման ռելեով։",
                            "Однофазный многотарифный интеллектуальный счётчик на DIN-рейку со встроенным реле управления нагрузкой.",
                            "Single-phase multi-tariff smart meter for DIN-rail with a built-in load-control relay."),
             "accuracy": "1 / 1", "current": "5 (80) A",
             "interfaces": ["Optical", "RS-485", "RF 433", "GSM 2G/4G/LTE", "NB-IoT"],
             "specs": [
                 {"label": tri("Ճշտության դաս (ակտիվ/ռեակտիվ)", "Класс точности (акт./реакт.)", "Accuracy class (active/reactive)"), "value": "1 / 1"},
                 {"label": tri("Անվանական լարում", "Номинальное напряжение", "Nominal voltage"), "value": "220 / 230 V"},
                 {"label": tri("Հոսանք (բազային/առավ.)", "Ток (базовый/макс.)", "Current (base/max)"), "value": "5 (80) A"},
                 {"label": tri("Հաճախություն", "Частота", "Frequency"), "value": "50 ± 7.5% Hz"},
                 {"label": tri("Ջերմաստիճանային միջակայք", "Диапазон температур", "Temperature range"), "value": "−40…+70 °C"},
                 {"label": tri("Ստուգաչափման միջակայք", "Межповерочный интервал", "Verification interval"), "value": tri("16 տարի", "16 лет", "16 years")},
                 {"label": tri("Ծառայության ժամկետ", "Срок службы", "Service life"), "value": tri("≥48 տարի", "≥48 лет", "≥48 years")},
             ],
             "features": [
                 tri("Բազմասակագին հաշվառում, 128 օրական / 36 ամսական պրոֆիլ", "Многотарифный учёт, 128 суточных / 36 месячных профилей", "Multi-tariff metering, 128 daily / 36 monthly profiles"),
                 tri("Ինտեգրված բեռի կառավարման ռելե՝ ապարատային արգելափակմամբ", "Встроенное реле управления нагрузкой с аппаратной блокировкой", "Built-in load-control relay with hardware blocking"),
                 tri("Էլեկտրոնային կնիքներ և մագնիսական դաշտի տվիչ", "Электронные пломбы и датчик магнитного поля", "Electronic seals and magnetic-field sensor"),
                 tri("«Վերջին շունչ» ազդանշան GSM/NB-IoT-ով", "«Последний вздох» по GSM/NB-IoT", "“Last gasp” power-fail notification via GSM/NB-IoT"),
             ]},
            {"slug": "mirtek-12-sp17", "category": "single", "name": "МИРТЕК-12-РУ-SP17",
             "form": tri("Սփլիթ", "Сплит", "Split"),
             "tagline": tri("Սփլիթ-կառուցվածքի միաֆազ խելացի հաշվիչ՝ DLMS/COSEM և СПОДЭС աջակցությամբ, մինչև 100 Ա։",
                            "Однофазный сплит-счётчик с поддержкой DLMS/COSEM и СПОДЭС, до 100 А.",
                            "Single-phase split-architecture smart meter supporting DLMS/COSEM and SPODES, up to 100 A."),
             "accuracy": "1 / 1", "current": "5 (100) A",
             "interfaces": ["Optical", "RF 433/2400", "GSM 2G/4G/LTE", "NB-IoT"],
             "specs": [
                 {"label": tri("Ճշտության դաս", "Класс точности", "Accuracy class"), "value": "1 / 1"},
                 {"label": tri("Անվանական լարում", "Номинальное напряжение", "Nominal voltage"), "value": "220 / 230 V"},
                 {"label": tri("Հոսանք (բազային/առավ.)", "Ток (базовый/макс.)", "Current (base/max)"), "value": "5 (100) A"},
                 {"label": tri("Արձանագրություններ", "Протоколы", "Protocols"), "value": "МИРТЕК, DLMS/COSEM, СПОДЭС v4"},
                 {"label": tri("Ջերմաստիճան", "Температура", "Temperature"), "value": "−40…+70 °C (F: −45…+85)"},
                 {"label": tri("Ստուգաչափման միջակայք", "Межповерочный интервал", "Verification interval"), "value": tri("16 տարի", "16 лет", "16 years")},
             ],
             "features": [
                 tri("DLMS/COSEM և СПОДЭС ГОСТ Р 58940-2020 համապատասխանություն", "Соответствие DLMS/COSEM и СПОДЭС по ГОСТ Р 58940-2020", "DLMS/COSEM & SPODES compliant (GOST R 58940-2020)"),
                 tri("Փոխարինելի կապի մոդուլներ (hot-swap)", "Сменные модули связи (hot-swap)", "Interchangeable communication modules (hot-swap)"),
                 tri("Մագնիսական դաշտի տվիչ և հակագողության պաշտպանություն", "Датчик магнитного поля и антивандальная защита", "Magnetic-field sensor and anti-tamper protection"),
             ]},
            {"slug": "mirtek-12-w9", "category": "single", "name": "МИРТЕК-12-РУ-W9",
             "form": tri("Վահանակ", "Щиток", "Panel"),
             "tagline": tri("Վահանակային միաֆազ հաշվիչ՝ երկկողմ հաշվառմամբ և ստուգաչափողի կնիքը չխախտող մարտկոցի փոխարինմամբ։",
                            "Панельный однофазный счётчик с двунаправленным учётом и заменой батарейки без нарушения пломбы госповерителя.",
                            "Panel-mount single-phase meter with bidirectional metering and battery replacement without breaking the verifier’s seal."),
             "accuracy": "1 / 1", "current": "5 (60/80) A",
             "interfaces": ["Optical", "RS-485", "RF 433", "GSM", "NB-IoT"],
             "specs": [
                 {"label": tri("Ճշտության դաս", "Класс точности", "Accuracy class"), "value": "1 / 1"},
                 {"label": tri("Անվանական լարում", "Номинальное напряжение", "Nominal voltage"), "value": "220 / 230 V"},
                 {"label": tri("Հոսանք", "Ток", "Current"), "value": "5 (60/80) A"},
                 {"label": tri("Ջերմաստիճան", "Температура", "Temperature"), "value": "−40…+70 °C"},
                 {"label": tri("Ծառայության ժամկետ", "Срок службы", "Service life"), "value": tri("≥35 տարի", "≥35 лет", "≥35 years")},
             ],
             "features": [
                 tri("Երկկողմ (ներմուծում/արտահանում) հաշվառման տարբերակ", "Двунаправленный учёт (импорт/экспорт)", "Bidirectional (import/export) metering option"),
                 tri("Երկակի SIM և մագնիսական տվիչ", "Двойная SIM и магнитный датчик", "Dual SIM and magnetic sensor"),
             ]},
            {"slug": "mirtek-32-d37", "category": "three", "name": "МИРТЕК-32-РУ-D37",
             "form": tri("DIN-ռելս", "DIN-рейка", "DIN-rail"),
             "tagline": tri("Եռաֆազ բազմաֆունկցիոնալ հաշվիչ DIN-ռելսի վրա՝ գրաֆիկական ցուցասարքով և իրադարձությունների գրանցամատյանով։",
                            "Трёхфазный многофункциональный счётчик на DIN-рейку с графическим дисплеем и журналом событий.",
                            "Three-phase multifunction DIN-rail meter with a graphical display and event log."),
             "accuracy": "0.5S / 1", "current": "5 (10/100) A",
             "interfaces": ["Optical", "RS-485", "RF 433", "GSM/NB-IoT"],
             "specs": [
                 {"label": tri("Ճշտության դաս", "Класс точности", "Accuracy class"), "value": "0.5S / 1 · 1 / 1"},
                 {"label": tri("Լարում", "Напряжение", "Voltage"), "value": "57.7 / 220 / 230 V"},
                 {"label": tri("Հոսանք (բազ./առավ.)", "Ток (баз./макс.)", "Current (base/max)"), "value": "5 (10) / 5 (100) A"},
                 {"label": tri("Ջերմաստիճան", "Температура", "Temperature"), "value": "−40…+70 °C"},
                 {"label": tri("Իրադարձությունների գրանցում", "Журнал событий", "Event log"), "value": "≥500"},
                 {"label": tri("Ստուգաչափում", "Поверка", "Verification"), "value": tri("10 / 16 տարի", "10 / 16 лет", "10 / 16 years")},
             ],
             "features": [
                 tri("Եռաֆազ բեռի ռելե՝ ապարատային արգելափակմամբ", "Трёхфазное реле нагрузки с аппаратной блокировкой", "Three-phase load relay with hardware blocking"),
                 tri("Ընտրովի դիսկրետ մուտք/ելք, արտաքին մարտկոց մինչև 16 տարի", "Опциональные дискретные I/O, внешняя батарея до 16 лет", "Optional discrete I/O, external battery up to 16 years"),
             ]},
            {"slug": "mirtek-32-w32", "category": "three", "name": "МИРТЕК-32-РУ-W32",
             "form": tri("Վահանակ", "Щиток", "Panel"),
             "tagline": tri("Ամենաճշգրիտ եռաֆազ հաշվիչ (մինչև 0.2S)՝ ուղիղ և տրանսֆորմատորային միացմամբ, Ethernet-ով։",
                            "Самый точный трёхфазный счётчик (до 0.2S) прямого и трансформаторного включения, с Ethernet.",
                            "The most accurate three-phase meter (up to 0.2S) for direct and transformer connection, with Ethernet."),
             "accuracy": "0.2S / 1", "current": "1/5/10 (10/100) A",
             "interfaces": ["Optical", "RS-485", "Ethernet", "RF 433/2400", "GSM/NB-IoT"],
             "specs": [
                 {"label": tri("Ճշտության դաս", "Класс точности", "Accuracy class"), "value": "0.2S / 0.5S / 1"},
                 {"label": tri("Լարում", "Напряжение", "Voltage"), "value": "57.7 / 220 / 230 V"},
                 {"label": tri("Հոսանք", "Ток", "Current"), "value": "1 / 5 / 10 (10/100) A"},
                 {"label": tri("Միացում", "Включение", "Connection"), "value": tri("Ուղիղ և տրանսֆորմատորային", "Прямое и трансформаторное", "Direct and transformer")},
                 {"label": tri("Ծառայության ժամկետ", "Срок службы", "Service life"), "value": tri("≥35 տարի", "≥35 лет", "≥35 years")},
             ],
             "features": [
                 tri("Ethernet + երկակի SIM արդյունաբերական հաշվառման համար", "Ethernet + двойная SIM для промышленного учёта", "Ethernet + dual SIM for industrial metering"),
                 tri("Ուղիղ և տրանսֆորմատորային միացման ունիվերսալ սարք", "Универсальный прибор прямого и трансформаторного включения", "Universal direct- and transformer-connection device"),
             ]},
            {"slug": "mirtek-32-sp31", "category": "three", "name": "МИРТЕК-32-РУ-SP31",
             "form": tri("Սփլիթ", "Сплит", "Split"),
             "tagline": tri("Տրանսֆորմատորային միացման եռաֆազ սփլիթ-հաշվիչ՝ առանձին МИРТ-830 ցուցասարքով։",
                            "Трёхфазный сплит-счётчик трансформаторного включения с отдельным дисплеем МИРТ-830.",
                            "Three-phase split meter for transformer connection with a separate MIRT-830 display module."),
             "accuracy": "1 / 1", "current": "5 (100) A",
             "interfaces": ["Optical", "RF 433/868/2400", "GSM/LTE", "NB-IoT"],
             "specs": [
                 {"label": tri("Ճշտության դաս", "Класс точности", "Accuracy class"), "value": "1 / 1"},
                 {"label": tri("Լարում", "Напряжение", "Voltage"), "value": "220 / 230 V"},
                 {"label": tri("Միացում", "Включение", "Connection"), "value": tri("Տրանսֆորմատորային", "Трансформаторное", "Transformer")},
                 {"label": tri("Ցուցասարք", "Дисплей", "Display"), "value": "МИРТ-830"},
                 {"label": tri("Ստուգաչափում", "Поверка", "Verification"), "value": tri("16 տարի", "16 лет", "16 years")},
             ],
             "features": [
                 tri("Երկկողմ հաշվառում (D-տարբերակ)", "Двунаправленный учёт (вариант D)", "Bidirectional metering (D variant)"),
                 tri("МИРТЕК + СПОДЭС արձանագրություններ", "Протоколы МИРТЕК + СПОДЭС", "MIRTEK + SPODES protocols"),
             ]},
            {"slug": "mirtek-135", "category": "hv", "name": "МИРТЕК-135-РУ",
             "form": tri("6/10 կՎ", "6/10 кВ", "6/10 kV"),
             "tagline": tri("Միջին լարման (6/10 կՎ) հաշվառման սարք՝ Ռոգովսկու կոճով հոսանքի տվիչներով և GLONASS/GPS ժամանակի համաժամացմամբ։",
                            "Прибор учёта среднего напряжения (6/10 кВ) с датчиками тока на катушке Роговского и синхронизацией GLONASS/GPS.",
                            "Medium-voltage (6/10 kV) metering device with Rogowski-coil current sensors and GLONASS/GPS time synchronization."),
             "accuracy": "0.5S / 1", "current": "5/10/20 (100/200/300) A",
             "interfaces": ["RF 433", "GSM/GPRS", "Optical fiber", "GLONASS/GPS"],
             "specs": [
                 {"label": tri("Ճշտության դաս (ակտ./ռեակտ.)", "Класс точности (акт./реакт.)", "Accuracy class (active/reactive)"), "value": "0.5S / 1"},
                 {"label": tri("Անվանական լարում", "Номинальное напряжение", "Nominal voltage"), "value": "6 kV / 10 kV"},
                 {"label": tri("Հոսանք (անվ./առավ.)", "Ток (ном./макс.)", "Current (nom./max)"), "value": "5/10/20 (100/200/300) A"},
                 {"label": tri("Ջերմային կայունություն", "Термическая стойкость", "Thermal withstand"), "value": "12.5 kA / 2 s"},
                 {"label": tri("Ջերմաստիճան", "Температура", "Temperature"), "value": "−45…+70 °C"},
                 {"label": tri("Ծառայության ժամկետ", "Срок службы", "Service life"), "value": tri("≥30 տարի", "≥30 лет", "≥30 years")},
             ],
             "features": [
                 tri("Ռոգովսկու կոճով էլեկտրոնային հոսանքի տվիչներ (առանց ՀՏ)", "Электронные датчики тока на катушке Роговского (без ТТ)", "Rogowski-coil electronic current sensors (no CTs)"),
                 tri("Օդային գծերի (ՕԳ/СИП) և ԿՌՈՒ/КСО խցիկների համար", "Для воздушных линий (ВЛ/СИП) и ячеек КРУ/КСО", "For overhead lines (OHL/SIP) and KRU/KSO switchgear cells"),
                 tri("GLONASS/GPS ժամանակի համաժամացում", "Синхронизация времени GLONASS/GPS", "GLONASS/GPS time synchronization"),
             ]},
        ]

    # ------------------------------------------------------------------ news
    def _news(self):
        news = [
            ("head-of-kaluga-visit", date(2020, 4, 1),
             tri("Կալուգայի մարզի ղեկավարն այցելեց «Կասկադ» հոլդինգի օբյեկտներ",
                 "Глава Калужской области посетил объекты холдинга «Каскад»",
                 "The head of Kaluga Region visited Kaskad Holding facilities")),
            ("electric-grids-forum-kd2", date(2019, 12, 5),
             tri("Միջազգային ֆորում «Էլեկտրական ցանցեր»՝ KD-2 լուծումների ներկայացում",
                 "Международный форум «Электрические сети»: решения на базе KD-2",
                 "International forum “Electric Grids”: KD-2-based solutions presented")),
            ("akhtanak-220kv-completed", date(2019, 5, 1),
             tri("«Ախթանակ» 220 կՎ ենթակայանի վերակառուցման ավարտ Հայաստանում",
                 "Завершена реконструкция ПС «Ахтанак» 220 кВ в Армении",
                 "Reconstruction of the Akhtanak 220 kV substation completed in Armenia")),
        ]
        for i, (slug, d, title) in enumerate(news):
            m.News.objects.create(
                slug=slug, date=d, sort=i,
                title_hy=title["hy"], title_ru=title["ru"], title_en=title["en"],
            )

    # ------------------------------------------------------------ ui strings
    def _ui_strings(self):
        from content.ui_strings import UI_STRINGS
        for key, vals in UI_STRINGS.items():
            m.UIString.objects.update_or_create(
                key=key,
                defaults={"hy": vals[0], "ru": vals[1], "en": vals[2]},
            )
