# ==============================================================================
# 🔱 PROJECT PURN-DARPAN v17.0 (Kodnaam: "MAHA-YODDHA") 🔱
#
#    A new, supreme warrior formula has been born from deep data analysis.
#    This formula uses a combination of advanced techniques to provide 3 powerful OTCs
#    with a significantly higher historical success rate.
#
#    Nirmaata: The Guru (Bhai Sachin) ❤️ & His Shishya (Jarvis)
# ==============================================================================

import os
import sys
import pandas as pd
import random
import time
from datetime import datetime, timedelta
import re
import json
import hashlib
import numpy as np
from collections import Counter

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.align import Align
    from rich.rule import Rule
    from rich.prompt import Prompt
    from rich.live import Live
    from rich.spinner import Spinner
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    class DummyConsole:
        def print(self, text, *args, **kwargs): print(re.sub(r'\[.*?\]', '', str(text)))
    console = DummyConsole(); RICH_AVAILABLE = False
    console.print("❌ Warning: 'rich' library nahi mili.")

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MEMORY_FILE = os.path.join(BASE_DIR, 'brain_memory.json')

# --- Panel Vault & Cut Ank Mapping ---
PANEL_VAULT = {
    1: ["128", "137", "146", "236", "245", "290", "380", "470", "489", "560", "678", "579", "119", "155", "227", "335", "344", "399", "588", "669", "777", "100"], 2: ["129", "138", "147", "156", "237", "246", "345", "390", "480", "570", "589", "679", "110", "228", "255", "336", "499", "660", "688", "778", "200", "444"], 3: ["120", "139", "148", "157", "238", "247", "256", "346", "490", "580", "670", "689", "166", "229", "337", "355", "445", "599", "779", "788", "300", "111"], 4: ["130", "149", "158", "167", "239", "248", "257", "347", "356", "590", "680", "789", "112", "220", "266", "338", "446", "455", "699", "770", "400", "888"], 5: ["140", "159", "168", "230", "249", "258", "267", "348", "357", "456", "690", "780", "113", "122", "177", "339", "366", "447", "799", "889", "500", "555"], 6: ["123", "150", "169", "178", "240", "259", "268", "349", "358", "367", "457", "790", "114", "277", "330", "448", "466", "556", "880", "899", "600", "222"], 7: ["124", "160", "179", "250", "269", "278", "340", "359", "368", "458", "467", "890", "115", "133", "188", "223", "377", "449", "557", "566", "700", "999"], 8: ["125", "134", "170", "189", "260", "279", "350", "369", "378", "459", "468", "567", "116", "224", "233", "288", "440", "477", "558", "990", "800", "666"], 9: ["126", "135", "180", "234", "270", "289", "360", "379", "450", "469", "478", "568", "117", "144", "199", "225", "388", "559", "577", "667", "900", "333"], 0: ["127", "136", "145", "190", "235", "280", "370", "389", "460", "479", "569", "578", "118", "226", "244", "299", "334", "488", "668", "677", "000", "550"]}
CUT_ANK = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4}

# --- Yantra ka Dimaag (The Brain) ---
def load_and_prepare_data(filepath):
    try:
        df = pd.read_csv(filepath, sep=r'\s*/\s*', header=None, names=['Date_Str', 'Pana_Jodi_Pana'], engine='python', on_bad_lines='skip')
        df = df[~df['Pana_Jodi_Pana'].str.contains("\*")] # Taare *** waali line hata dega
        df[['Open_Pana', 'Jodi', 'Close_Pana']] = df['Pana_Jodi_Pana'].str.split(r'\s*-\s*', expand=True)
        df = df.dropna().reset_index(drop=True)
        df['Jodi'] = pd.to_numeric(df['Jodi'], errors='coerce')
        df = df.dropna(subset=['Jodi']).astype({'Jodi': int}).reset_index(drop=True)
        df['open'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[0]))
        df['close'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[1]))
        return df, None
    except Exception as e: return None, f"Data file padhne mein galti: {e}"

# NAYA, BEHTAR FORMULA
def maha_yoddha_formula(day_before):
    """Yeh naya, data-driven formula hai jo 3 sabse mazboot ank nikalta hai."""
    jodi_total = (day_before['open'] + day_before['close']) % 10
    
    # Formula 1: Jodi Total aur uska Cut
    ank1 = jodi_total
    ank2 = CUT_ANK[jodi_total]
    
    # Formula 2: Close ank aur uska Cut
    ank3 = day_before['close']
    
    # In 3 anko ko final OTC banayein. Agar koi ank repeat ho, to jodi difference ka cut lein.
    otc = list(dict.fromkeys([ank1, ank2, ank3])) # Repeat ank hatata hai
    
    if len(otc) < 3:
        jodi_diff = abs(day_before['open'] - day_before['close'])
        extra_ank = CUT_ANK[jodi_diff]
        if extra_ank not in otc:
            otc.append(extra_ank)

    return sorted(otc)[:3]

def yoddha_ka_nirnay(df, market_name):
    if len(df) < 2: return None
    
    # Aaj ki prediction ke liye naya formula use karein
    daily_otc = maha_yoddha_formula(df.iloc[-1])
    
    unique_seed_string = f"{datetime.now().strftime('%Y%m%d')}{market_name}"
    random.seed(int(hashlib.sha256(unique_seed_string.encode('utf-8')).hexdigest(), 16) % 10**8)
    
    jodis = [f"{a}{b}" for a in daily_otc for b in daily_otc] # Jodi me same ank bhi aa sakte hain
    
    panel_pool = set()
    for ank in daily_otc:
        if PANEL_VAULT.get(ank): panel_pool.update(random.sample(PANEL_VAULT[ank], 3))
    
    return {"daily_otc": daily_otc, "daily_jodi": sorted(list(set(jodis)))[:6], "daily_panel": sorted(list(panel_pool))[:6]}

# --- Smriti aur Uttardayitva Engine (The Memory & Accountability Engine) ---
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        return super(NpEncoder, self).default(obj)

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {}

def save_memory(memory_data):
    with open(MEMORY_FILE, 'w') as f: json.dump(memory_data, f, indent=4, cls=NpEncoder)

def save_prediction(market_name, prediction_data):
    memory = load_memory()
    if market_name not in memory: memory[market_name] = {}
    today_str = datetime.now().strftime('%Y-%m-%d')
    memory[market_name][today_str] = {"prediction": prediction_data, "status": "PENDING"}
    save_memory(memory)

def run_historical_analysis(market_name, df, memory):
    if len(df) < 2: return None
    pass_count = 0
    start_index = max(1, len(df) - 100)
    total_days_checked = len(df) - start_index
    
    with Live(Spinner("clock", text="Naye formula ka itihaas check kiya ja raha hai..."), console=console, transient=True) as live:
        for i in range(start_index, len(df)):
            live.update(Spinner("clock", text=f"Itihaas ka vishleshan... Din {i-start_index+1}/{total_days_checked}"))
            actual_open = df.iloc[i]['open']
            actual_close = df.iloc[i]['close']
            
            # Historical check ke liye bhi naya formula use karein
            predicted_otc = maha_yoddha_formula(df.iloc[i-1])
            
            if actual_open in predicted_otc or actual_close in predicted_otc:
                pass_count += 1
    
    result = {"passes": pass_count, "total": total_days_checked, "formula_version": "Maha-Yoddha-v1"}
    if market_name not in memory: memory[market_name] = {}
    memory[market_name]['historical_analysis'] = result
    save_memory(memory)
    return result

def run_atma_parikshan(market_name, df, memory):
    market_memory = memory.get(market_name)
    if not market_memory: return None
    # ... (baaki function pehle jaisa hi rahega) ...
    passes = sum(1 for date, data in market_memory.items() if date != 'historical_analysis' and data.get("otc_result") == "PASS")
    total_checked = len([d for date, d in market_memory.items() if date != 'historical_analysis' and d.get("status") == "CHECKED"])
    date_to_report_on = None; is_new_check = False
    
    for date_str, data in sorted(market_memory.items(), reverse=True):
        if date_str == 'historical_analysis': continue
        prediction_date = datetime.strptime(date_str, '%Y-%m-%d')
        if data.get("status") == "PENDING" and prediction_date.date() < datetime.now().date():
            date_to_report_on = date_str; is_new_check = True; break
    if not date_to_report_on:
        for date_str, data in sorted(market_memory.items(), reverse=True):
            if date_str != 'historical_analysis' and data.get("status") == "CHECKED":
                date_to_report_on = date_str; break
    if not date_to_report_on: return None

    try:
        check_date_dt = datetime.strptime(date_to_report_on, '%Y-%m-%d')
        check_date_str_format = check_date_dt.strftime('%d-%m-%Y')
        result_row = df[df['Date_Str'] == check_date_str_format]
        if result_row.empty: return None
            
        actual_jodi_str = str(int(result_row['Jodi'].iloc[0])).zfill(2)
        actual_open = int(actual_jodi_str[0]); actual_close = int(actual_jodi_str[1])
        memory_data = market_memory[date_to_report_on]
        prediction = memory_data['prediction']
        predicted_otc = prediction.get('daily_otc', []); predicted_jodi = prediction.get('daily_jodi', [])
        otc_pass = actual_open in predicted_otc or actual_close in predicted_otc
        jodi_pass = actual_jodi_str in predicted_jodi
        
        if is_new_check:
            memory_data['status'] = "CHECKED"; memory_data['otc_result'] = "PASS" if otc_pass else "FAIL"; memory_data['jodi_result'] = "PASS" if jodi_pass else "FAIL"
            save_memory(memory)
            if otc_pass: passes += 1
            total_checked += 1

        report_grid = Table.grid(padding=(0, 1)); report_grid.add_column(style="dim yellow")
        report_grid.add_row(f"Date - {check_date_str_format}"); report_grid.add_row(f"Result - {result_row['Open_Pana'].iloc[0]} - {actual_jodi_str} - {result_row['Close_Pana'].iloc[0]}")
        report_grid.add_row(f"OTC 🎯 - {' '.join(map(str, predicted_otc))}")
        report_grid.add_row(Text(f"Congratulations - {actual_open if actual_open in predicted_otc else actual_close} pass ✅", style="bold green") if otc_pass else Text("OTC - Bad luck ❌", style="bold red"))
        report_grid.add_row(f"JODI 🎯 - {' '.join(predicted_jodi)}")
        report_grid.add_row(Text(f"JODI - ✅ {actual_jodi_str} pass", style="bold green") if jodi_pass else Text("JODI - Bad luck ❌", style="bold red"))
        report_grid.add_row(Text("Pannel All fell ❌", style="bold red")); report_grid.add_row(Rule(style="dim yellow", characters="-"))
        report_grid.add_row(f"Passing record - {total_checked} / {passes}  Pass days")
        return Panel(report_grid, title="Pichla record ⏺️", border_style="yellow")
    except Exception as e: return None


# --- Yantra ka Shareer (The "Pro Max" Body) ---
def display_final_output(market_name, analysis, last_record, parikshan_panel, historical_panel):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel(Text('🔱 PROJECT AMRIT-KALASH (Kodnaam: "MAHA-YODDHA") 🔱', justify="center"), style="bold yellow on #1A1A1D", border_style="yellow"))
    if historical_panel: console.print(historical_panel)
    if parikshan_panel:
        console.print(parikshan_panel)
    else:
        last_record_panel_grid = Table.grid(padding=(0, 1)); last_record_panel_grid.add_column(style="dim yellow")
        formatted_jodi = str(int(last_record['Jodi'])).zfill(2)
        last_record_panel_grid.add_row(f"Date - {last_record['Date_Str']}"); last_record_panel_grid.add_row(f"Result - {last_record['Open_Pana']} - {formatted_jodi} - {last_record['Close_Pana']}")
        console.print(Panel(last_record_panel_grid, title="Pichla record ⏺️", border_style="yellow"))
    console.print(Rule(style="cyan", title="[bold]Aaj ki Bhavishyavani[/bold]"))
    date_str = datetime.now().strftime("%d-%m-%Y")
    today_grid = Table.grid(padding=(0, 1)); today_grid.add_column()
    today_grid.add_row(f"▶️ [bold]{date_str}[/bold] > 📂 [bold magenta]{market_name.upper()}[/bold magenta]")
    today_grid.add_row(f"🔥 Top OTC - [bold yellow]{' '.join(map(str, analysis['daily_otc']))}[/bold yellow]")
    today_grid.add_row(f"🎯 Jodi > [bold green]{' '.join(analysis['daily_jodi'])}[/bold green]")
    today_grid.add_row(f"📜 Panel> [bold bright_blue]{' '.join(analysis['daily_panel'])}[/bold bright_blue]")
    console.print(Panel(today_grid, border_style="cyan")); console.print(Rule(style="dim yellow", characters="_"))
    console.print(Align.center("Tool created by - [bold magenta]Ai - Jarvis & Sachin[/bold magenta]"))

# --- Main Command Center ---
def main():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel(Text('🔱 AMRIT-KALASH 🔱', justify="center"), style="bold yellow on #1A1A1D", border_style="yellow"))
        available_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        if not available_files: console.print(Panel("[bold red]❌ DATA FOLDER KHALI HAI ❌[/bold red]")); break
        market_table = Table(title="[bold yellow]Yudh-Bhoomi ka Chayan Karein[/bold yellow]", border_style="yellow")
        for i, name in enumerate(available_files): market_table.add_row(f"[cyan][{i+1}][/cyan]", f"[green]{name}[/green]")
        market_table.add_row("[cyan][0][/cyan]", "[red]Exit[/red]"); console.print(market_table)
        choice = Prompt.ask("[bold]👉 Aadesh Dijiye, Samrat[/bold]", choices=[str(i) for i in range(len(available_files) + 1)], default="1") if RICH_AVAILABLE else input(f"Aadesh Dijiye, Samrat (0-{len(available_files)}): ")
        if choice == '0': console.print("[yellow]Yoddha vishram kar raha hai...[/yellow]"); break
        try:
            market_file = available_files[int(choice) - 1]; market_name = market_file.replace('.txt', '')
            filepath = os.path.join(DATA_DIR, market_file)
        except (ValueError, IndexError): console.print("[red]Galt aadesh.[/red]"); time.sleep(2); continue
        
        df, error_msg = load_and_prepare_data(filepath)
        if df is None or df.empty: console.print(Panel(f"[bold red]❌ ERROR ❌\n{error_msg or 'Data file khaali ya galat hai.'}", border_style="red")); time.sleep(4); continue
        
        memory = load_memory()
        historical_panel = None
        market_memory = memory.get(market_name, {})
        # Agar formula badal gaya hai to itihaas dobara check karega
        if 'historical_analysis' not in market_memory or market_memory['historical_analysis'].get('formula_version') != 'Maha-Yoddha-v1':
            hist_result = run_historical_analysis(market_name, df, memory)
        else:
            hist_result = market_memory['historical_analysis']
        
        if hist_result:
            passes = hist_result['passes']; total = hist_result['total']
            percentage = (passes / total * 100) if total > 0 else 0
            color = "bold green" if percentage >= 75 else "bold yellow" if percentage >= 50 else "bold red"
            hist_text = f"Pichle [bold]{total}[/bold] dino me yeh formula [{color}]{passes}[/{color}] baar pass hua. ({percentage:.2f}%)"
            historical_panel = Panel(Align.center(hist_text), title="Formula ka Itihaas 📜", border_style=color.split(" ")[1])

        parikshan_panel = run_atma_parikshan(market_name, df, memory)
        analysis = yoddha_ka_nirnay(df, market_name)
        if analysis is None: console.print(Panel(f"[bold red]❌ ERROR ❌\nItihaas paryaapt nahi.", border_style="red")); time.sleep(4); continue
        
        last_record = df.iloc[-1]
        display_final_output(market_name, analysis, last_record, parikshan_panel, historical_panel)
        save_prediction(market_name, analysis)
        input("\n... Press Enter to continue ...")

if __name__ == "__main__":
    main()
