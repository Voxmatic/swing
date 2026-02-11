from data.fetcher import TVFetcher
from engine.motion_line import MotionEngine
from engine.price_engine import PriceEngine
from engine.time_phase3 import TimePhase3
from engine.bias_phase import BiasPhase

from bb_weekly_filter import passes_weekly_bb
from rsi_filter import passes_rsi_filter


# ------------------------
# CONFIG
# ------------------------
EXCHANGE = "NSE"
BARS = 300

SYMBOLS = [
    "NIFTY","BANKNIFTY","360ONE","3MINDIA","ABB","ACC","ACMESOLAR","AIAENG","APLAPOLLO","AUBANK","AWL","AADHARHFC","AARTIIND","AAVAS","ABBOTINDIA","ACE","ADANIENSOL","ADANIENT","ADANIGREEN","ADANIPORTS","ADANIPOWER","ATGL","ABCAPITAL","ABFRL","ABLBL","ABREL","ABSLAMC","AEGISLOG","AEGISVOPAK","AFCONS","AFFLE","AJANTPHARM","AKUMS","AKZOINDIA","APLLTD","ALKEM","ALKYLAMINE","ALOKINDS","ARE&M","AMBER","AMBUJACEM","ANANDRATHI","ANANTRAJ","ANGELONE","APARINDS","APOLLOHOSP","APOLLOTYRE","APTUS","ASAHIINDIA","ASHOKLEY","ASIANPAINT","ASTERDM","ASTRAZEN","ASTRAL","ATHERENERG","ATUL","AUROPHARMA","AIIL","DMART","AXISBANK","BASF","BEML","BLS","BSE","BAJAJ-AUTO","BAJFINANCE","BAJAJFINSV","BAJAJHLDNG","BAJAJHFL","BALKRISIND","BALRAMCHIN","BANDHANBNK","BANKBARODA","BANKINDIA","MAHABANK","BATAINDIA","BAYERCROP","BERGEPAINT","BDL","BEL","BHARATFORG","BHEL","BPCL","BHARTIARTL","BHARTIHEXA","BIKAJI","BIOCON","BSOFT","BLUEDART","BLUEJET","BLUESTARCO","BBTC","BOSCHLTD","FIRSTCRY","BRIGADE","BRITANNIA","MAPMYINDIA","CCL","CESC","CGPOWER","CRISIL","CAMPUS","CANFINHOME","CANBK","CAPLIPOINT","CGCL","CARBORUNIV","CASTROLIND","CEATLTD","CENTRALBK","CDSL","CENTURYPLY","CERA","CHALET","CHAMBLFERT","CHENNPETRO","CHOICEIN","CHOLAHLDNG","CHOLAFIN","CIPLA","CUB","CLEAN","COALINDIA","COCHINSHIP","COFORGE","COHANCE","COLPAL","CAMS","CONCORDBIO","CONCOR","COROMANDEL","CRAFTSMAN","CREDITACC","CROMPTON","CUMMINSIND","CYIENT","DCMSHRIRAM","DLF","DOMS","DABUR","DALBHARAT","DATAPATTNS","DEEPAKFERT","DEEPAKNTR","DELHIVERY","DEVYANI","DIVISLAB","DIXON","AGARWALEYE","LALPATHLAB","DRREDDY","DUMMYHDLVR","EIDPARRY","EIHOTEL","EICHERMOT","ELECON","ELGIEQUIP","EMAMILTD","EMCURE","ENDURANCE","ENGINERSIN","ERIS","ESCORTS","ETERNAL","EXIDEIND","NYKAA","FEDERALBNK","FACT","FINCABLES","FINPIPE","FSL","FIVESTAR","FORCEMOT","FORTIS","GAIL","GVT&D","GMRAIRPORT","GRSE","GICRE","GILLETTE","GLAND","GLAXO","GLENMARK","MEDANTA","GODIGIT","GPIL","GODFRYPHLP","GODREJAGRO","GODREJCP","GODREJIND","GODREJPROP","GRANULES","GRAPHITE","GRASIM","GRAVITA","GESHIP","FLUOROCHEM","GUJGASLTD","GMDCLTD","GSPL","HEG","HBLENGINE","HCLTECH","HDFCAMC","HDFCBANK","HDFCLIFE","HFCL","HAPPSTMNDS","HAVELLS","HEROMOTOCO","HEXT","HSCL","HINDALCO","HAL","HINDCOPPER","HINDPETRO","HINDUNILVR","HINDZINC","POWERINDIA","HOMEFIRST","HONASA","HONAUT","HUDCO","HYUNDAI","ICICIBANK","ICICIGI","ICICIPRULI","IDBI","IDFCFIRSTB","IFCI","IIFL","INOXINDIA","IRB","IRCON","ITCHOTELS","ITC","ITI","INDGN","INDIACEM","INDIAMART","INDIANB","IEX","INDHOTEL","IOC","IOB","IRCTC","IRFC","IREDA","IGL","INDUSTOWER","INDUSINDBK","NAUKRI","INFY","INOXWIND","INTELLECT","INDIGO","IGIL","IKS","IPCALAB","JBCHEPHARM","JKCEMENT","JBMA","JKTYRE","JMFINANCIL","JSWENERGY","JSWINFRA","JSWSTEEL","JPPOWER","J&KBANK","JINDALSAW","JSL","JINDALSTEL","JIOFIN","JUBLFOOD","JUBLINGREA","JUBLPHARMA","JWL","JYOTHYLAB","JYOTICNC","KPRMILL","KEI","KPITTECH","KSB","KAJARIACER","KPIL","KALYANKJIL","KARURVYSYA","KAYNES","KEC","KFINTECH","KIRLOSBROS","KIRLOSENG","KOTAKBANK","KIMS","LTF","LTTS","LICHSGFIN","LTFOODS","LTIM","LT","LATENTVIEW","LAURUSLABS","THELEELA","LEMONTREE","LICI","LINDEINDIA","LLOYDSME","LODHA","LUPIN","MMTC","MRF","MGL","MAHSCOOTER","MAHSEAMLES","M&MFIN","M&M","MANAPPURAM","MRPL","MANKIND","MARICO","MARUTI","MFSL","MAXHEALTH","MAZDOCK","METROPOLIS","MINDACORP","MSUMI","MOTILALOFS","MPHASIS","MCX","MUTHOOTFIN","NATCOPHARM","NBCC","NCC","NHPC","NLCINDIA","NMDC","NSLNISP","NTPCGREEN","NTPC","NH","NATIONALUM","NAVA","NAVINFLUOR","NESTLEIND","NETWEB","NEULANDLAB","NEWGEN","NAM-INDIA","NIVABUPA","NUVAMA","NUVOCO","OBEROIRLTY","ONGC","OIL","OLAELEC","OLECTRA","PAYTM","ONESOURCE","OFSS","POLICYBZR","PCBL","PGEL","PIIND","PNBHOUSING","PTCIL","PVRINOX","PAGEIND","PATANJALI","PERSISTENT","PETRONET","PFIZER","PHOENIXLTD","PIDILITIND","PPLPHARMA","POLYMED","POLYCAB","POONAWALLA","PFC","POWERGRID","PRAJIND","PREMIERENE","PRESTIGE","PGHH","PNB","RRKABEL","RBLBANK","RECLTD","RHIM","RITES","RADICO","RVNL","RAILTEL","RAINBOW","RKFORGE","RCF","REDINGTON","RELIANCE","RELINFRA","RPOWER","SBFC","SBICARD","SBILIFE","SJVN","SKFINDIA","SRF","SAGILITY","SAILIFE","SAMMAANCAP","MOTHERSON","SAPPHIRE","SARDAEN","SAREGAMA","SCHAEFFLER","SCHNEIDER","SCI","SHREECEM","SHRIRAMFIN","SHYAMMETL","ENRIN","SIEMENS","SIGNATURE","SOBHA","SOLARINDS","SONACOMS","SONATSOFTW","STARHEALTH","SBIN","SAIL","SUMICHEM","SUNPHARMA","SUNTV","SUNDARMFIN","SUNDRMFAST","SUPREMEIND","SUZLON","SWANCORP","SWIGGY","SYNGENE","SYRMA","TBOTEK","TVSMOTOR","TATACHEM","TATACOMM","TCS","TATACONSUM","TATAELXSI","TATAINVEST","TMPV","TATAPOWER","TATASTEEL","TATATECH","TTML","TECHM","TECHNOE","TEJASNET","NIACL","RAMCOCEM","THERMAX","TIMKEN","TITAGARH","TITAN","TORNTPHARM","TORNTPOWER","TARIL","TRENT","TRIDENT","TRIVENI","TRITURBINE","TIINDIA","UCOBANK","UNOMINDA","UPL","UTIAMC","ULTRACEMCO","UNIONBANK","UBL","UNITDSPR","USHAMART","VGUARD","DBREALTY","VTL","VBL","MANYAVAR","VEDL","VENTIVE","VIJAYA","VMM","IDEA","VOLTAS","WAAREEENER","WELCORP","WELSPUNLIV","WHIRLPOOL","WIPRO","WOCKPHARMA","YESBANK","ZFCVINDIA","ZEEL","ZENTEC","ZENSARTECH","ZYDUSLIFE","ECLERX"
]

tv = TVFetcher()


# ======================================================
# MAIN SCAN FUNCTION (Streamlit will call this)
# ======================================================
def run_scan():

    bullish_stocks = []

    for SYMBOL in SYMBOLS:

        # ---------------- BB FILTER ----------------
        try:
            if not passes_weekly_bb(SYMBOL):
                continue
        except:
            continue

        # ---------------- FETCH DATA ----------------
        try:
            df = tv.fetch_daily(SYMBOL, EXCHANGE, BARS)
        except:
            continue

        if df is None or df.empty or len(df) < 50:
            continue

        # ---------------- RSI FILTER ----------------
        rsi_ok, _ = passes_rsi_filter(df)
        if not rsi_ok:
            continue

        # ---------------- NRT ENGINE ----------------
        motion_engine = MotionEngine()
        price_engine = PriceEngine()
        time_engine = TimePhase3()
        bias_engine = BiasPhase()

        price_state = None
        time_state = None
        bias_state = None

        for _, row in df.iterrows():
            motion_engine.process_bar(row)

            price_state = price_engine.update(
                row.C,
                motion_engine.state.tp_sequence
            )

            time_state = time_engine.update(
                row,
                motion_engine.state.tp_sequence
            )

            bias_state = bias_engine.update(
                row,
                motion_engine.state.tp_sequence
            )

        # ---------------- FINAL CONDITION ----------------
        if (
            (price_state == "POSITIVE" and time_state == "POSITIVE") or
            (price_state == "POSITIVE" and bias_state == "POSITIVE")
        ):
            bullish_stocks.append({
                "symbol": SYMBOL,
                "price": price_state,
                "time": time_state,
                "bias": bias_state,
                "close": float(df.iloc[-1].C)
            })

    return bullish_stocks
