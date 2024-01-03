import time
import datetime
import telebot
import requests
import re
import codecs
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse 
from urllib.parse import unquote
from os import getenv

# Initialize the bot with your token
bot = telebot.TeleBot("6923585464:AAHCOf8QQtiyPvmX4B_X5PFJhu82VfkwPrA", threaded=True)

setlan = None
usernum = 0
timer = 0
command_executed = False
      
country_codes = {
    "AF": "Afghanistan",
    "AX": "Åland Islands",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antarctica",
    "AG": "Antigua and Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BV": "Bouvet Island",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory",
    "BN": "Brunei Darussalam",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "CV": "Cape Verde",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CX": "Christmas Island",
    "CC": "Cocos (Keeling) Islands",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo",
    "CD": "Congo, The Democratic Republic of the",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "CI": "Côte d'Ivoire",
    "HR": "Croatia",
    "CU": "Cuba",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FK": "Falkland Islands (Malvinas)",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "PF": "French Polynesia",
    "TF": "French Southern Territories",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HM": "Heard Island and McDonald Islands",
    "VA": "Holy See (Vatican City State)",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran, Islamic Republic of",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KP": "Korea, Democratic People's Republic of",
    "KR": "Korea, Republic of",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Lao People's Democratic Republic",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LY": "Libyan Arab Jamahiriya",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macao",
    "MK": "Macedonia, The Former Yugoslav Republic of",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia, Federated States of",
    "MD": "Moldova, Republic of",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "MM": "Myanmar",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands",
    "AN": "Netherlands Antilles",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger",
    "NG": "Nigeria",
    "NU": "Niue",
    "NF": "Norfolk Island",
    "MP": "Northern Mariana Islands",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PS": "Palestinian Territory, Occupied",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines",
    "PN": "Pitcairn",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "BL": "Saint Barthélemy",
    "SH": "Saint Helena",
    "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia",
    "MF": "Saint Martin",
    "PM": "Saint Pierre and Miquelon",
    "VC": "Saint Vincent and the Grenadines",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "Sao Tome and Principe",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "ZA": "South Africa",
    "GS": "South Georgia and the South Sandwich Islands",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "SD": "Sudan",
    "SR": "Suriname",
    "SJ": "Svalbard and Jan Mayen",
    "SZ": "Swaziland",
    "SE": "Sweden",
    "CH": "Switzerland",
    "SY": "Syrian Arab Republic",
    "TW": "Taiwan, Province of China",
    "TJ": "Tajikistan",
    "TZ": "Tanzania, United Republic of",
    "TH": "Thailand",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TK": "Tokelau",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TM": "Turkmenistan",
    "TC": "Turks and Caicos Islands",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "US": "United States",
    "UM": "United States Minor Outlying Islands",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VE": "Venezuela",
    "VN": "Viet Nam",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.S.",
    "WF": "Wallis and Futuna",
    "EH": "Western Sahara",
    "YE": "Yemen",
    "ZM": "Zambia",
    "ZW": "Zimbabwe",
}


country_codes_ar = {
    "AF": "أفغانستان",
    "AX": "جزر آلاند",
    "AL": "ألبانيا",
    "DZ": "الجزائر",
    "AS": "ساموا الأمريكية",
    "AD": "أندورا",
    "AO": "أنغولا",
    "AI": "أنغيلا",
    "AQ": "القارة القطبية الجنوبية",
    "AG": "أنتيغوا وباربودا",
    "AR": "الأرجنتين",
    "AM": "أرمينيا",
    "AW": "أروبا",
    "AU": "أستراليا",
    "AT": "النمسا",
    "AZ": "أذربيجان",
    "BS": "جزر البهاما",
    "BH": "البحرين",
    "BD": "بنغلاديش",
    "BB": "باربادوس",
    "BY": "بيلاروسيا",
    "BE": "بلجيكا",
    "BZ": "بليز",
    "BJ": "بنين",
    "BM": "برمودا",
    "BT": "بوتان",
    "BO": "بوليفيا",
    "BA": "البوسنة والهرسك",
    "BW": "بوتسوانا",
    "BV": "جزيرة بوفيت",
    "BR": "البرازيل",
    "IO": "الإقليم البريطاني في المحيط الهندي",
    "BN": "بروناي",
    "BG": "بلغاريا",
    "BF": "بوركينا فاسو",
    "BI": "بوروندي",
    "KH": "كمبوديا",
    "CM": "الكاميرون",
    "CA": "كندا",
    "CV": "الرأس الأخضر",
    "KY": "جزر كايمان",
    "CF": "جمهورية أفريقيا الوسطى",
    "TD": "تشاد",
    "CL": "شيلي",
    "CN": "الصين",
    "CX": "جزيرة عيد الميلاد",
    "CC": "جزر كوكوس (كيلينج)",
    "CO": "كولومبيا",
    "KM": "جزر القمر",
    "CG": "الكونغو",
    "CD": "جمهورية الكونغو الديمقراطية",
    "CK": "جزر كوك",
    "CR": "كوستاريكا",
    "CI": "ساحل العاج",
    "HR": "كرواتيا",
    "CU": "كوبا",
    "CY": "قبرص",
    "CZ": "الجمهورية التشيكية",
    "DK": "الدنمارك",
    "DJ": "جيبوتي",
    "DM": "دومينيكا",
    "DO": "جمهورية الدومينيكان",
    "EC": "الإكوادور",
    "EG": "مصر",
    "SV": "السلفادور",
    "GQ": "غينيا الاستوائية",
    "ER": "إريتريا",
    "EE": "إستونيا",
    "ET": "إثيوبيا",
    "FK": "جزر فوكلاند (مالفيناس)",
    "FO": "جزر فارو",
    "FJ": "فيجي",
    "FI": "فنلندا",
    "FR": "فرنسا",
    "GF": "غويانا الفرنسية",
    "PF": "بولينزيا الفرنسية",
    "TF": "المناطق الجنوبية لفرنسا",
    "GA": "الغابون",
    "GM": "غامبيا",
    "GE": "جورجيا",
    "DE": "ألمانيا",
    "GH": "غانا",
    "GI": "جبل طارق",
    "GR": "اليونان",
    "GL": "جرينلاند",
    "GD": "غرينادا",
    "GP": "جوادلوب",
    "GU": "غوام",
    "GT": "غواتيمالا",
    "GG": "جيرنزي",
    "GN": "غينيا",
    "GW": "غينيا بيساو",
    "GY": "غيانا",
    "HT": "هايتي",
    "HM": "جزيرة هيرد وجزر ماكدونالد",
    "VA": "الفاتيكان",
    "HN": "هندوراس",
    "HK": "هونغ كونغ",
    "HU": "هنغاريا",
    "IS": "آيسلندا",
    "IN": "الهند",
    "ID": "إندونيسيا",
    "IR": "إيران",
    "IQ": "العراق",
    "IE": "أيرلندا",
    "IM": "جزيرة مان",
    "IL": "إسرائيل",
    "IT": "إيطاليا",
    "JM": "جامايكا",
    "JP": "اليابان",
    "JE": "جيرسي",
    "JO": "الأردن",
    "KZ": "كازاخستان",
    "KE": "كينيا",
    "KI": "كيريباتي",
    "KP": "كوريا الشمالية",
    "KR": "كوريا الجنوبية",
    "KW": "الكويت",
    "KG": "قيرغيزستان",
    "LA": "جمهورية لاو الديمقراطية الشعبية",
    "LV": "لاتفيا",
    "LB": "لبنان",
    "LS": "ليسوتو",
    "LR": "ليبيريا",
    "LY": "ليبيا",
    "LI": "ليختنشتاين",
    "LT": "ليتوانيا",
    "LU": "لوكسمبورج",
    "MO": "ماكاو",
    "MK": "مقدونيا، جمهورية يوغوسلافيا السابقة",
    "MG": "مدغشقر",
    "MW": "ملاوي",
    "MY": "ماليزيا",
    "MV": "جزر المالديف",
    "ML": "مالي",
    "MT": "مالطا",
    "MH": "جزر مارشال",
    "MQ": "مارتينيك",
    "MR": "موريتانيا",
    "MU": "موريشيوس",
    "YT": "مايوت",
    "MX": "المكسيك",
    "FM": "ولايات ميكرونيزيا الموحدة",
    "MD": "جمهورية مولدوفا",
    "MC": "موناكو",
    "MN": "منغوليا",
    "ME": "الجبل الأسود",
    "MS": "مونتسرات",
    "MA": "المغرب",
    "MZ": "موزمبيق",
    "MM": "ميانمار",
    "NA": "ناميبيا",
    "NR": "ناورو",
    "NP": "نيبال",
    "NL": "هولندا",
    "NC": "كاليدونيا الجديدة",
    "NZ": "نيوزيلندا",
    "NI": "نيكاراغوا",
    "NE": "النيجر",
    "NG": "نيجيريا",
    "NU": "نيوي",
    "NF": "جزيرة نورفولك",
    "MP": "جزر ماريانا الشمالية",
    "NO": "النرويج",
    "OM": "عمان",
    "PK": "باكستان",
    "PW": "بالاو",
    "PS": "الأراضي الفلسطينية المحتلة",
    "PA": "بنما",
    "PG": "بابوا غينيا الجديدة",
    "PY": "باراغواي",
    "PE": "بيرو",
    "PH": "الفلبين",
    "PN": "بيتكيرن",
    "PL": "بولندا",
    "PT": "البرتغال",
    "PR": "بورتو ريكو",
    "QA": "قطر",
    "RE": "لا ريونيون",
    "RO": "رومانيا",
    "RU": "الاتحاد الروسي",
    "RW": "رواندا",
    "BL": "سان بارتيليمي",
    "SH": "سانت هيلينا",
    "KN": "سانت كيتس ونيفيس",
    "LC": "سانت لوسيا",
    "MF": "سانت مارتن (الجزء الهولندي)",
    "PM": "سانت بيير وميكلون",
    "VC": "سانت فينسنت وجزر غرينادين",
    "WS": "ساموا",
    "SM": "سان مارينو",
    "ST": "ساو تومي وبرينسيبي",
    "SA": "المملكة العربية السعودية",
    "SN": "السنغال",
    "RS": "صربيا",
    "SC": "سيشل",
    "SL": "سيراليون",
    "SG": "سنغافورة",
    "SK": "سلوفاكيا",
    "SI": "سلوفينيا",
    "SB": "جزر سليمان",
    "SO": "الصومال",
    "ZA": "جمهورية جنوب إفريقيا",
    "GS": "جورجيا الجنوبية وجزر ساندويتش الجنوبية",
    "ES": "إسبانيا",
    "LK": "سريلانكا",
    "SD": "السودان",
    "SR": "سورينام",
    "SJ": "سفالبارد وجان ماين",
    "SZ": "سوازيلاند",
    "SE": "السويد",
    "CH": "سويسرا",
    "SY": "الجمهورية العربية السورية",
    "TW": "تايوان، جمهورية الصين",
    "TJ": "طاجيكستان",
    "TZ": "تانزانيا، جمهورية المتحدة",
    "TH": "تايلاند",
    "TL": "تيمور الشرقية",
    "TG": "توغو",
    "TK": "توكيلو",
    "TO": "تونغا",
    "TT": "ترينيداد وتوباغو",
    "TN": "تونس",
    "TR": "تركيا",
    "TM": "تركمانستان",
    "TC": "جزر تركس وكايكوس",
    "TV": "توفالو",
    "UG": "أوغندا",
    "UA": "أوكرانيا",
    "AE": "الإمارات العربية المتحدة",
    "GB": "المملكة المتحدة",
    "US": "الولايات المتحدة",
    "UM": "جزر الولايات المتحدة البعيدة الصغيرة",
    "UY": "الأورغواي",
    "UZ": "أوزبكستان",
    "VU": "فانواتو",
    "VE": "فنزويلا",
    "VN": "فيتنام",
    "VG": "جزر فيرجن البريطانية",
    "VI": "جزر فيرجن الأمريكية",
    "WF": "والس وفوتونا",
    "EH": "الصحراء الغربية",
    "YE": "اليمن",
    "ZM": "زامبيا",
    "ZW": "زيمبابوي",
    }

language_codes = {
    "en": "English",
    "ar": "Arabic",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "ru": "Russian",
    "zh": "Chinese",
    "hi": "Hindi",
    "pt": "Portuguese",
    "tr": "Turkish",
    "ko": "Korean",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "zh-CN": "Mandarin",
    "zh-HK": "Cantonese",
    "nl": "Dutch",
    "cs": "Czech",
    "pl": "Polish",
    "hu": "Hungarian",
    "ro": "Romanian",
    "hr": "Croatian",
    "sl": "Slovenian",
    "sr": "Serbian",
    "el": "Greek",
    "he": "Hebrew",
    "da": "Danish",
    "sv": "Swedish",
    "fi": "Finnish",
    "no": "Norwegian",
    "is": "Icelandic",
    "et": "Estonian",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "ku": "Kurdish",
    "az": "Azerbaijani",
    "uk": "Ukrainian",
    "ka": "Georgian",
    "hy": "Armenian",
    "bg": "Bulgarian",
    "sr-Latn": "Serbian (Latin)",
}

language_codes_ar = {
    "en": "الإنجليزية",
    "ar": "العربية",
    "fr": "الفرنسية",
    "es": "الإسبانية",
    "de": "الألمانية",
    "it": "الإيطالية",
    "ja": "اليابانية",
    "ru": "الروسية",
    "zh": "الصينية",
    "hi": "الهندية",
    "pt": "البرتغالية",
    "tr": "التركية",
    "ko": "الكورية",
    "th": "التايلاندية",
    "vi": "الفيتنامية",
    "id": "الإندونيسية",
    "zh-CN": "الماندرين",
    "zh-HK": "الكانتونية",
    "nl": "الهولندية",
    "cs": "التشيكية",
    "pl": "البولندية",
    "hu": "المجرية",
    "ro": "الرومانية",
    "hr": "الكرواتية",
    "sl": "السلوفينية",
    "sr": "الصربية",
    "el": "اليونانية",
    "he": "العبرية",
    "da": "الدنماركية",
    "sv": "السويدية",
    "fi": "الفنلندية",
    "no": "النرويجية",
    "is": "الأيسلندية",
    "et": "الإستونية",
    "lv": "اللاتفية",
    "lt": "اللتوانية",
    "ku": "الكردي",
    "az": "الأذرية",
    "uk": "الأوكرانية",
    "ka": "الجورجية",
    "hy": "الأرمنية",
    "bg": "البلغارية",
    "sr-Latn": "الصربية (لاتينية)",
}


def make_request(url, user_agent):
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    return response
    
def decode_unicode(value):
    return bytes(value, 'utf-8').decode('unicode-escape')

@bot.message_handler(regexp=r'https?://[^\s]+')
def extract_url(message):
   timerv = 0
   global setlan  # قم بتعريف المتغير كـ global لاستخدامه لاحقًا
   if setlan == "ar":
        down_meg = "جاري تنزيل الفيديو...."
        done = "✅ عملية المعالجة"
   elif setlan == "en":
        down_meg = "Downloading video...."
        done = "✅ Treatment process"
   if setlan is None:
        user = message.from_user
        markup = telebot.types.InlineKeyboardMarkup()
        english_button = telebot.types.InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = telebot.types.InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
   else:
       wait_message = bot.send_message(message.chat.id, f"{done}\n{down_meg}\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")
       url_tiktok = message.text.strip()
       bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜")
       headers = {
           "Content-Type": "application/json",
           "cache-control": "no-cache, no-store, max-age=0, must-revalidate",
       }
       bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜")
       data = {
           "url": f"{url_tiktok}"
       }
       bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜")
       url = "https://www.veed.io/video-downloader-ap/api/download-content"
       response = requests.post(url, headers=headers, json=data)
       
       if response.status_code == 200:
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"{done}\n{down_meg}\n🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜")
           response_data = response.json()
           
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜")
           title = response_data.get("title", "")
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜")
           username = response_data.get("username", "")
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜")
           media = response_data.get("media", [])
           bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                     text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜")

           if media:
               first_media_url = media[0].get("url", "")
               media_format = media[0].get("format", "")
               cleaned_media_url = first_media_url.replace("/video-downloader-ap/api/stream-media?url=", "")
               cleaned_media_url_decoded = unquote(cleaned_media_url)
               bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id,
                                                   text=f"{done}\n{down_meg}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩")
               print(cleaned_media_url)
               if setlan == "en":
                    caption_text = f"Video Title: <code>{title}</code>\nVideo owner's account name: <code>{username}</code>"
               elif setlan == "ar":
                    caption_text = f"عنوان الفيديو: <code>{title}</code>\nاسم حساب مالك الفيديو: <code>{username}</code>"
               bot.send_video(message.chat.id, cleaned_media_url_decoded, caption=caption_text, parse_mode='HTML')

       else:
           if setlan == "en":
              bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"There is a problem with the link!\n      \n🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥")
           elif setlan == "ar":
              bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"هناك مشكلة في الرابط!\n      \n🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥")

@bot.message_handler(commands=['start'])
def start(message):
    if setlan is None:
        user = message.from_user
        markup = InlineKeyboardMarkup()
        english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
    elif setlan == "ar":
       
        bot.send_message(message.chat.id, "مرحبا, أنا بوت تلجرام متعدد الأدوات لي التيكتوك\n ارسل /help لكي  تري كيف تستعملني.")
    elif setlan == "en":
        bot.send_message(message.chat.id, "Hello, I am a multi-tool Telegram bot for Tiktok.\n Send /help to see how to use me.")

@bot.message_handler(commands=['help'])
def start(message):
    if setlan is None:
        user = message.from_user
        markup = InlineKeyboardMarkup()
        english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
    elif setlan == "ar":
        bot.send_message(message.chat.id, "للحصول علي معلومات حساب التيكتوك فقط قم بارسال اليوزر.\n لتنزيل فيديو بدون علامه مائيه فقط قم بارسال الرابط.")
    elif setlan == "en":
        bot.send_message(message.chat.id, "To obtain Tiktok account information, just send the user.\n To download a video without a watermark, just send the link.")


@bot.message_handler(commands=['language'])
def choose_language(message):
    user = message.from_user
    markup = InlineKeyboardMarkup()
    english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
    arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
    markup.add(english_button, arabic_button)
    helloen = "Please choose your language 🇬🇧"
    helloar = "الرجاء اختيار لغتك 🇪🇬"
    bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global setlan

    if call.data == 'en':
        bot.answer_callback_query(call.id, text="You chose English 🇬🇧")
        setlan = "en"
        bot.send_message(call.message.chat.id, "Hello, I am a multi-tool Telegram bot for Tiktok.\n Send /help to see how to use me.")
    elif call.data == 'ar':
        bot.answer_callback_query(call.id, text="اخترت العربية 🇪🇬")
        setlan = "ar"
        bot.send_message(call.message.chat.id, "        مرحبا, أنا بوت تلجرام متعدد الأدوات لي التيكتوك\n ارسل /help لكي  تري كيف تستعملني.")

@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    if setlan is None:
        user = message.from_user
        markup = InlineKeyboardMarkup()
        english_button = InlineKeyboardButton("English 🇬🇧", callback_data='en')
        arabic_button = InlineKeyboardButton("العربية 🇪🇬", callback_data='ar')
        markup.add(english_button, arabic_button)
        helloen = "Please choose your language 🇬🇧"
        helloar = "الرجاء اختيار لغتك 🇪🇬"
        bot.send_message(message.chat.id, f"{helloen}\n{helloar}", reply_markup=markup)
    else:
        username = message.text
        url = f"https://www.tiktok.com/@{username}"
        user_agent = "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36"
        response = make_request(url, user_agent)

        if response.status_code == 200:
            text = response.text
            if "userInfo" in text:
                if setlan == "ar":
                     wait_m = f"✅ عملية المعالجة"
                elif setlan == "en":
                     wait_m = f"✅ Treatment process"
                info_message = bot.send_message(message.chat.id, f"{wait_m}\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜")
                text = text.replace('''https:"''', '')
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜")
                text = text.replace('''},"stats":{''', ',')
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜")
                start_word = '''userInfo":{"user":{"'''
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜")
                end_word = """},"itemList":[]},"shareMeta"""
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜")
                pattern = re.compile(f'{re.escape(start_word)}(.*?){re.escape(end_word)}', re.IGNORECASE | re.DOTALL)
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜")
                match = pattern.search(text)
                data = match.group(1) if match else None
                result_text = data.replace("""https:""", '')
                data = result_text[:-1]
                decoded_data = urllib.parse.unquote(data)
                lines = decoded_data.split(',')
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜")

                # تعريف المتغيرات واستخراج البيانات
                user_id = unique_id = nickname = avatar_larger = signature = create_time = verified = sec_uid = ""
                relation = private_account = is_ad_virtual = unique_modify_time = tt_seller = region = ""
                following_visibility = is_embed_banned = language = following_count = heart_count = video_count = ""
                friend_count = bio_link = ""
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜")
                # استخراج وتخزين البيانات
                for line in lines:
                    pairs = line.split(':')
                    key = pairs[0].strip('"{}')
                    value = pairs[1].strip('"{}')
                    add = "https:"

                    if key in ["avatarLarger"]:
                        value = add + decode_unicode(value)

                    if key == "id":
                        user_id = value
                    elif key == "uniqueId":
                        unique_id = value
                    elif key == "nickname":
                        nickname = value
                    elif key == "avatarLarger":
                        avatar_larger = value
                    elif key == "signature":
                        signature = value
                    elif key == "createTime":
                        create_time = value
                        if create_time == "0":
                            if setlan == "en":
                                create_time = "unknown"
                            else:
                                create_time = "غير معروف"
                    elif key == "verified":
                        verified = value
                        if verified == "true":
                            if setlan == "en":
                                verified = "yes"
                            else:
                                verified = "نعم"
                        else:
                            if setlan == "en":
                                verified = "no"
                            else:
                                verified = "لا"
                    elif key == "secUid":
                        sec_uid = value
                    elif key == "relation":
                        relation = value
                        if relation == "0":
                            if setlan == "en":
                                relation = "not found"
                            else:
                                relation = "لا يوجد"
                    elif key == "privateAccount":
                        private_account = value
                        if private_account == "true":
                            if setlan == "en":
                                private_account = "yes"
                            else:
                                private_account = "نعم"
                        else:
                            if setlan == "en":
                                private_account = "no"
                            else:
                                private_account = "لا"
                    elif key == "isADVirtual":
                        is_ad_virtual = value
                        if is_ad_virtual == "true":
                            if setlan == "en":
                                is_ad_virtual = "yes"
                            else:
                                is_ad_virtual = "نعم"
                        else:
                            if setlan == "en":
                                is_ad_virtual = "no"
                            else:
                                is_ad_virtual = "لا"
                    elif key == "uniqueIdModifyTime":
                        unique_modify_time = value
                        if unique_modify_time == "0":
                            if setlan == "en":
                                unique_modify_time = "unknown"
                            else:
                                unique_modify_time = "غير معروف"
                    elif key == "ttSeller":
                        tt_seller = value
                        if tt_seller == "true":
                            if setlan == "en":
                                tt_seller = "yes"
                            else:
                                tt_seller = "نعم"
                        else:
                            if setlan == "en":
                                tt_seller = "no"
                            else:
                                tt_seller = "لا"
                    elif key == "region":
                        regione = value
                        if setlan == "en":
                          region = country_codes.get(regione, "unknown")
                        else:
                          region = country_codes_ar.get(regione, "غير معروفه")
                    elif key == "followingVisibility":
                        following_visibility = value
                        if following_visibility == 1:
                           if setlan == en:
                              following_visibility = "opend"
                           else:
                              following_visibility = "مفتوحه"
                        else:
                           if setlan == "en":
                              following_visibility = "closed"
                           else:
                              following_visibility = "مقفوله"
                    elif key == "isEmbedBanned":
                        is_embed_banned = value
                        if is_embed_banned == "true":
                            if setlan == "en":
                                is_embed_banned = "yes"
                            else:
                                is_embed_banned = "نعم"
                        else:
                            if setlan == "en":
                                isEmbedBanned = "no"
                            else:
                                isEmbedBanned = "لا"
                    elif key == "language":
                        language_codee = value
                        if setlan == "en":
                          language = language_codes.get(language_codee, "unknown")
                        else:
                          language = language_codes_ar.get(language_codee, "غير معروفه")
                    elif key == "followerCount":
                        follower_count = value
                        print(follower_count)
                    elif key == "followingCount":
                        following_count = value
                    elif key == "heartCount":
                        heart_count = value
                    elif key == "videoCount":
                        video_count = value
                    elif key == "friendCount":
                        friend_count = value
                    elif key == "bioLink":
                        bio_link = value
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜")
                if bio_link == "":
                  if setlan == "en":
                      bio_link = "not found"
                  else:
                      bio_link = "غير موجود"
                global infoen
                global infoar
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜")
                infoar = (
    f"🔵 معرف المستخدمᬊᬁ\n X✯<code>{user_id}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌟 اسم المستخدم الفريدᬊᬁ\n X✯<code>{unique_id}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 الاسم المستعارᬊᬁ\n X✯<code>{nickname}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🖼️ صورة الملف الشخصيᬊᬁ\n X✯<code>{avatar_larger}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💬 السيرة الذاتيةᬊᬁ\n X✯<code>{signature}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕒 وقت إنشاء الحسابᬊᬁ\n X✯<code>{create_time}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔐 هل الحساب موثقᬊᬁ\n X✯<code>{verified}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔑 هوية فريدة أخرىᬊᬁ\n X✯<code>{sec_uid}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💑 علاقات الحساباتᬊᬁ\n X✯<code>{relation}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔗 رابط السيرة الذاتيةᬊᬁ\n X✯<code>{bio_link}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👁️ رؤية المتابعينᬊᬁ\n X✯<code>{following_visibility}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔒 هل الحساب خاصᬊᬁ\n X✯<code>{private_account}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌐 هل الحساب إعلان افتراضيᬊᬁ\n X✯<code>{is_ad_virtual}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕰️ وقت تعديل الهوية الفريدةᬊᬁ\n X✯<code>{unique_modify_time}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💼 هل الحساب تجاريᬊᬁ\n X✯<code>{tt_seller}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌍 المنطقةᬊᬁ\n X✯<code>{region}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🚫 حظر التضمينᬊᬁ\n X✯<code>{is_embed_banned}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🗣️ اللغةᬊᬁ\n X✯<code>{language}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👥 عدد المتابعينᬊᬁ\n X✯<code>{follower_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 عدد المتابعين الذين يتم متابعتهمᬊᬁ\n X✯<code>{following_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"❤️ عدد الإعجاباتᬊᬁ\n X✯<code>{heart_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📹 عدد الفيديوهاتᬊᬁ\n X✯<code>{video_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👫 عدد الأصدقاءᬊᬁ\n X✯<code>{friend_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪"
)

                infoen = (
    f"🔵 User IDᬊᬁ\nع✯<code>{user_id}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌟 Unique usernameᬊᬁ\nع✯<code>{unique_id}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 Nicknameᬊᬁ\nع✯<code>{nickname}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🖼️ Profile pictureᬊᬁ\nع✯<code>{avatar_larger}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💬 Bioᬊᬁ\nع✯<code>{signature}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕒 Account creation timeᬊᬁ\nع✯<code>{create_time}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔐 Is account verifiedᬊᬁ\nع✯<code>{verified}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔑 Another unique identityᬊᬁ\nع✯<code>{sec_uid}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💑 Account relationshipsᬊᬁ\nع✯<code>{relation}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔗 Bio linkᬊᬁ\nع✯<code>{bio_link}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👁️ Following visibilityᬊᬁ\nع✯<code>{following_visibility}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🔒 Is account privateᬊᬁ\nع✯<code>{private_account}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌐 Is account virtual ADᬊᬁ\nع✯<code>{is_ad_virtual}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🕰️ Unique ID modification timeᬊᬁ\nع✯<code>{unique_modify_time}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"💼 Is account commercialᬊᬁ\nع✯<code>{tt_seller}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🌍 Regionᬊᬁ\nع✯<code>{region}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🚫 Embed banᬊᬁ\nع✯<code>{is_embed_banned}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"🗣️ Languageᬊᬁ\nع✯<code>{language}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👥 Follower countᬊᬁ\nع✯<code>{follower_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👤 Following countᬊᬁ\nع✯<code>{following_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"❤️ Like countᬊᬁ\nع✯<code>{heart_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"📹 Video countᬊᬁ\nع✯<code>{video_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪\t \n    \n"
    f"👫 Friend countᬊᬁ\nع✯<code>{friend_count}</code>✯\n        \n✤H࿐e࿐x࿐4≪"
)
                bot.edit_message_text(chat_id=message.chat.id, message_id=info_message.message_id, text=f"{wait_m}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩")
                bot.delete_message(chat_id=message.chat.id, message_id=info_message.message_id)
                bot.send_photo(message.chat.id, requests.get(avatar_larger).content)       
                if setlan == "en":
                    bot.send_message(message.chat.id, text=infoen, parse_mode='HTML')
                elif setlan == "ar":
                    bot.send_message(message.chat.id, text=infoar, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, "المستخدم غير موجود")
        else:
            bot.send_message(message.chat.id, f"فشلت الطلب برمز الحالة: {response.status_code}")

if __name__ == "__main__":
    # Set webhook
    bot.remove_webhook()
    bot.set_webhook(url=getenv("webhook"))

    # Start polling
    bot.polling()
