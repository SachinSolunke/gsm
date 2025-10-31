# ==============================================================================
# 🔱 PROJECT PURN-DARPAN v19.1 (Kodnaam: "TARKASH") 🔱
#
#    The Yantra now holds a Quiver (Tarkash) of multiple powerful formulas.
#    Before predicting, it performs "Aatm-Parikshan" by backtesting all formulas
#    on historical data to choose the "Champion Arrow" for the day.
#    (Markup error corrected for flawless performance)
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

# --- Configuration & Mappings ---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MEMORY_FILE = os.path.join(BASE_DIR, 'brain_memory.json')
CUT_ANK = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4}

# --- Yantra ka Dimaag (The Brain) ---
def load_and_prepare_data(filepath):
    try:
        df = pd.read_csv(filepath, sep=r'\s*/\s*', header=None, names=['Date_Str', 'Pana_Jodi_Pana'], engine='python', on_bad_lines='skip')
        df = df[~df['Pana_Jodi_Pana'].str.contains("\*")]
        df[['Open_Pana', 'Jodi', 'Close_Pana']] = df['Pana_Jodi_Pana'].str.split(r'\s*-\s*', expand=True)
        df = df.dropna().reset_index(drop=True)
        df['Jodi'] = pd.to_numeric(df['Jodi'], errors='coerce')
        df = df.dropna(subset=['Jodi']).astype({'Jodi': int}).reset_index(drop=True)
        df['open'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[0]))
        df['close'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[1]))
        df['Date'] = pd.to_datetime(df['Date_Str'], format='%d-%m-%Y')
        df['weekday'] = df['Date'].dt.day_name()
        return df, None
    except Exception as e: return None, f"Data file padhne mein galti: {e}"

# ==============================================================================
# 🏹 FORMULA TARKASH (THE QUIVER OF FORMULAS) 🏹
# ==============================================================================

def formula_maha_yoddha(day_before):
    jodi_total = (day_before['open'] + day_before['close']) % 10
    otc = list(dict.fromkeys([jodi_total, CUT_ANK[jodi_total], day_before['close']]))
    if len(otc) < 3:
        jodi_diff = abs(day_before['open'] - day_before['close'])
        otc.append(CUT_ANK[jodi_diff])
    return sorted(list(set(otc)))[:3]

def formula_jodi_diff_master(day_before):
    jodi_diff = abs(day_before['open'] - day_before['close'])
    otc = list(dict.fromkeys([jodi_diff, CUT_ANK[jodi_diff], day_before['open']]))
    if len(otc) < 3:
        jodi_total = (day_before['open'] + day_before['close']) % 10
        otc.append(jodi_total)
    return sorted(list(set(otc)))[:3]

def formula_open_close_cut(day_before):
    otc = list(dict.fromkeys([day_before['open'], day_before['close'], CUT_ANK[day_before['open']]]))
    return sorted(otc)[:3]
    
FORMULA_TARKASH = {
    "Maha-Yoddha": formula_maha_yoddha,
    "Jodi-Diff Master": formula_jodi_diff_master,
    "Open-Close Cut": formula_open_close_cut
}

# ==============================================================================
# 🎯 SARVASHRESHTH TEER KA CHAYAN (BEST ARROW SELECTOR) 🎯
# ==============================================================================

def find_best_formula(df, memory, market_name):
    market_memory = memory.get(market_name, {})
    if 'champion_formula' in market_memory:
        champion_name = market_memory['champion_formula']['name']
        if champion_name in FORMULA_TARKASH:
            return FORMULA_TARKASH[champion_name], market_memory['champion_formula']

    best_formula_name, best_score, total_days = None, -1, 0
    with Live(Spinner("clock", text="Sabhi formula ka aatm-parikshan ho raha hai..."), console=console, transient=True) as live:
        for name, formula_func in FORMULA_TARKASH.items():
            pass_count = 0
            start_index = max(1, len(df) - 100)
            total_days = len(df) - start_index
            for i in range(start_index, len(df)):
                day_before, actual_open, actual_close = df.iloc[i-1], df.iloc[i]['open'], df.iloc[i]['close']
                predicted_otc = formula_func(day_before)
                if actual_open in predicted_otc or actual_close in predicted_otc: pass_count += 1
            if pass_count > best_score: best_score, best_formula_name = pass_count, name
    pass_percentage = (best_score / total_days * 100) if total_days > 0 else 0
    champion_data = {"name": best_formula_name, "score": best_score, "total": total_days, "rate": f"{pass_percentage:.2f}%"}
    if market_name not in memory: memory[market_name] = {}
    memory[market_name]['champion_formula'] = champion_data
    save_memory(memory)
    return FORMULA_TARKASH[best_formula_name], champion_data

# --- Helper Functions ---
def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return {}

def save_memory(memory_data):
    with open(MEMORY_FILE, 'w') as f: json.dump(memory_data, f, indent=4)

# --- Main UI Functions ---
# YAHAN Galti Theek Ki Gayi Hai
def run_daily_prediction(market_name, df, memory):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel(f"🔱 [bold]Roz ka Anuman[/bold] - {market_name.upper()} 🔱", style="bold yellow on #1A1A1D"))
    champion_formula_func, champion_data = find_best_formula(df, memory, market_name)
    rate_value = float(champion_data['rate'][:-1])
    score_color = "green" if rate_value >= 75 else "yellow" if rate_value >= 50 else "red"
    
    # YEH LINE THEEK KI GAYI HAI: [/{score_color}] ki jagah [/bold {score_color}]
    report_text = f"Pichle {champion_data['total']} dino ke aadhar par, sabse safal formula hai:\n\n" \
                  f"🏹 [bold cyan]{champion_data['name']}[/bold cyan]\n" \
                  f"🎯 Safalta Dar: [bold {score_color}]{champion_data['rate']}[/bold {score_color}] ({champion_data['score']}/{champion_data['total']} din pass)"
    
    console.print(Panel(Align.center(report_text), title="Formula ka Aatm-Parikshan 🎯", border_style=score_color))
    
    prediction_otc = champion_formula_func(df.iloc[-1])
    jodis = sorted(list(set([f"{a}{b}" for a in prediction_otc for b in prediction_otc])))[:6]
    
    console.print(Rule(style="cyan", title="[bold]Aaj ki Bhavishyavani[/bold]"))
    date_str = datetime.now().strftime("%d-%m-%Y")
    today_grid = Table.grid(padding=(0, 1)); today_grid.add_column()
    today_grid.add_row(f"▶️ [bold]{date_str}[/bold] > 📂 [bold magenta]{market_name.upper()}[/bold magenta]")
    today_grid.add_row(f"🔥 Top OTC - [bold yellow]{' '.join(map(str, prediction_otc))}[/bold yellow]")
    today_grid.add_row(f"🎯 Jodi > [bold green]{' '.join(jodis)}[/bold green]")
    console.print(Panel(today_grid, border_style="cyan"))
    input("\n... Press Enter to continue ...")

def run_weekly_analysis(market_name, df):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel(f"🔱 [bold]Saptahik Vishleshan[/bold] - {market_name.upper()} 🔱", style="bold yellow on #1A1A1D"))
    if len(df) < 28:
        console.print("[red]Saptahik vishleshan ke liye paryaapt data nahi hai (kam se kam 28 din chahiye).[/red]")
        time.sleep(3); return
    last_4_weeks = df.tail(28)
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    table = Table(title="Pichle 4 Hafton me Har Din ke 'Hot' Ank", border_style="cyan")
    table.add_column("Din", style="bold magenta", justify="right")
    table.add_column("Open me Hot", style="yellow")
    table.add_column("Close me Hot", style="green")
    table.add_column("Jodi me Hot", style="bright_blue")
    for day in week_days:
        day_df = last_4_weeks[last_4_weeks['weekday'] == day]
        if not day_df.empty:
            open_hot = day_df['open'].mode().tolist()
            close_hot = day_df['close'].mode().tolist()
            jodi_hot = pd.concat([day_df['open'], day_df['close']]).mode().tolist()
            table.add_row(day, str(open_hot), str(close_hot), str(jodi_hot))
    console.print(table)
    input("\n... Press Enter to continue ...")

# --- Main Command Center ---
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel(Text('🔱 AMRIT-KALASH (TARKASH) 🔱', justify="center"), style="bold yellow on #1A1A1D", border_style="yellow"))
        menu_table = Table(title="[bold yellow]Karya ka Chayan Karein[/bold yellow]", border_style="yellow")
        menu_table.add_row("[cyan][1][/cyan]", "[green]Daily Prediction (Roz ka Anuman)[/green]")
        menu_table.add_row("[cyan][2][/cyan]", "[cyan]Weekly Analysis (Saptahik Vishleshan)[/cyan]")
        menu_table.add_row("[cyan][0][/cyan]", "[red]Exit (VISHRAM)[/red]")
        console.print(menu_table)
        choice = Prompt.ask("[bold]👉 Aadesh Dijiye[/bold]", choices=["1", "2", "0"], default="1")
        if choice == '0': break
        available_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        if not available_files: console.print(Panel("[bold red]❌ DATA FOLDER KHALI HAI ❌[/bold red]")); time.sleep(3); continue
        market_table = Table(title="[bold yellow]Yudh-Bhoomi ka Chayan Karein[/bold yellow]", border_style="yellow")
        for i, name in enumerate(available_files): market_table.add_row(f"[cyan][{i+1}][/cyan]", f"[green]{name}[/green]")
        console.print(market_table)
        market_choice = Prompt.ask("[bold]👉 Market Chunein[/bold]", choices=[str(i) for i in range(1, len(available_files) + 1)], default="1")
        try:
            market_file = available_files[int(market_choice) - 1]; market_name = market_file.replace('.txt', '')
            filepath = os.path.join(DATA_DIR, market_file)
            df, error_msg = load_and_prepare_data(filepath)
            if df is None or df.empty:
                console.print(Panel(f"[bold red]❌ ERROR ❌\n{error_msg or 'Data file khaali ya galat hai.'}", border_style="red")); time.sleep(4); continue
            memory = load_memory()
            if choice == '1':
                run_daily_prediction(market_name, df, memory)
            elif choice == '2':
                run_weekly_analysis(market_name, df)
        except (ValueError, IndexError):
            console.print("[red]Galt aadesh.[/red]"); time.sleep(2); continue
    console.print("[yellow]Yoddha vishram kar raha hai...[/yellow]")

if __name__ == "__main__":
    main()
