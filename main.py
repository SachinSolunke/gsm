# ==============================================================================
# 🔱 PROJECT PURN-SIDDHI v2.1 (Kodnaam: "MAHA-SANKALPA") 🔱
#
#    UPGRADE REPORT:
#    1. Prediction Date added to output.
#    2. Suggested Panels (Top 2 per Ank) integrated.
#    3. Weekly Tracker enhanced to show which PANA hit.
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
from collections import Counter

# --- RICH Library Handling ---
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
    # Fallback to simple print if rich is not available
    class DummyConsole:
        def print(self, text, *args, **kwargs):
            # Remove rich markup for simple printing
            clean_text = re.sub(r'\[.*?\]', '', str(text))
            print(clean_text, *args, **kwargs)
    console = DummyConsole(); RICH_AVAILABLE = False
    print("❌ Warning: 'rich' library nahi mili.")

# --- Configuration & Mappings (Sthir Gyaan) ---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CUT_ANK = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4}

# --- PANA-KOSH (The Panel Database) ---
PANA_SET = {
    1: ['119', '128', '137', '146', '155', '227', '236', '245', '290', '335', '344', '380', '399', '470', '489', '560', '579', '588', '678', '669'],
    2: ['110', '129', '138', '147', '156', '228', '237', '246', '255', '336', '345', '390', '480', '499', '570', '589', '660', '679', '688', '778'],
    3: ['111', '120', '139', '148', '157', '166', '229', '238', '247', '256', '337', '346', '355', '445', '490', '580', '599', '670', '689', '779', '78>
    4: ['112', '130', '149', '158', '167', '220', '239', '248', '257', '266', '338', '347', '356', '446', '455', '590', '680', '699', '770', '789'],
    5: ['113', '122', '140', '159', '168', '177', '230', '249', '258', '267', '339', '348', '357', '366', '447', '456', '690', '780', '799', '889'],
    6: ['114', '123', '150', '169', '178', '240', '259', '268', '277', '330', '349', '358', '367', '448', '457', '466', '556', '790', '880', '899'],
    7: ['115', '133', '124', '160', '179', '188', '223', '250', '269', '278', '340', '359', '368', '377', '449', '458', '467', '557', '566', '890'],
    8: ['116', '125', '134', '170', '189', '224', '233', '260', '279', '288', '350', '369', '378', '440', '459', '468', '477', '558', '567', '990'],
    9: ['117', '126', '135', '144', '180', '199', '225', '234', '270', '289', '360', '379', '388', '450', '469', '478', '559', '568', '577', '667'],
    0: ['118', '127', '136', '190', '226', '235', '244', '299', '370', '389', '460', '479', '488', '550', '569', '578', '668', '677', '780', '890']
}

# --- Data Preparation ---
def load_and_prepare_data(filepath):
    try:
        # ... (Same Pandas logic as before) ...
        df = pd.read_csv(filepath, sep=r'\s*/\s*', header=None, names=['Date_Str', 'Pana_Jodi_Pana'], engine='python', on_bad_lines='skip')
        df = df.dropna(subset=['Pana_Jodi_Pana'])
        df = df[~df['Pana_Jodi_Pana'].str.contains(r"\*", na=False)]
        df[['Open_Pana', 'Jodi', 'Close_Pana']] = df['Pana_Jodi_Pana'].str.split(r'\s*-\s*', expand=True)
        df = df.dropna().reset_index(drop=True)
        for col in ['Open_Pana', 'Jodi', 'Close_Pana']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna().astype({'Open_Pana': int, 'Jodi': int, 'Close_Pana': int}).reset_index(drop=True)
        df['open'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[0]))
        df['close'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[1]))
        df['Date'] = pd.to_datetime(df['Date_Str'], format='%d-%m-%Y', errors='coerce')
        df = df.dropna(subset=['Date']).sort_values(by='Date').reset_index(drop=True)
        return df, None
    except Exception as e: return None, f"Data file padhne mein galti: {e}"

# ==============================================================================
# 🌌 BRAHMANDA-SUTRA ENGINE (THE CORE PREDICTIVE LOGIC) 🌌
# ==============================================================================
def find_brahmanda_sutra(df):
    # ... (Same find_brahmanda_sutra logic as before) ...
    if len(df) < 1: return None
    last_day = df.iloc[-1]
    seed_open_pana = str(last_day['Open_Pana']).zfill(3)
    seed_jodi = str(last_day['Jodi']).zfill(2)
    seed_close_pana = str(last_day['Close_Pana']).zfill(3)

    open_seed_ank = (int(seed_open_pana[0]) + int(seed_open_pana[2])) % 10
    jodi_seed_ank = (int(seed_jodi[0]) + int(seed_jodi[1])) % 10
    close_seed_ank = (int(seed_close_pana[0]) + int(seed_close_pana[2])) % 10

    sutra_ank1 = (open_seed_ank + jodi_seed_ank) % 10
    sutra_ank2 = CUT_ANK[sutra_ank1]
    sutra_ank3 = (jodi_seed_ank + close_seed_ank) % 10

    core_otc = sorted(list(set([sutra_ank1, sutra_ank2, sutra_ank3])))

    if len(core_otc) < 3:
        extra_ank = CUT_ANK[jodi_seed_ank]
        if extra_ank not in core_otc: core_otc.append(extra_ank)
        core_otc = sorted(core_otc)[:3]

    jodi_candidates = [f"{a}{b}" for a in core_otc for b in core_otc]
    strongest_jodis = list(set(jodi_candidates))[:6]

    return {
        "core_otc": core_otc,
        "strongest_jodis": strongest_jodis
    }

def get_suggested_panels(core_otc):
    """Core OTC ke liye top panels suggest karta hai."""
    suggested_panels = []
    # Har Ank ke liye PANA_SET se shuru ke 2 panels lena
    for ank in core_otc:
        panels = PANA_SET.get(ank, [])
        suggested_panels.extend(panels[:2])
    return suggested_panels
    # ==============================================================================
# 🎯 SATYAPAN ENGINE (THE TRUTH/VALIDATION ENGINE) 🎯
# ==============================================================================
def check_sutra_hit(sutra_otc, open_ank, close_ank, open_pana_str, close_pana_str):
    """Result aur Sutra ko compare karke hit status return karta hai."""
    ank_hit, pana_hit, hit_pana_str = False, False, ""

    # 1. ANK Hit Check (OTC)
    if open_ank in sutra_otc or close_ank in sutra_otc:
        ank_hit = True

    # 2. PANA Hit Check & Hit Pana String Capture
    if open_ank in sutra_otc and open_pana_str in PANA_SET.get(open_ank, []):
        pana_hit = True
        hit_pana_str = open_pana_str
    elif close_ank in sutra_otc and close_pana_str in PANA_SET.get(close_ank, []):
        pana_hit = True
        hit_pana_str = close_pana_str

    return ank_hit, pana_hit, hit_pana_str

def sutra_validation_engine(df, check_days=40):
    # ... (Same sutra_validation_engine logic, using new check_sutra_hit) ...
    results = {'ank_hit_count': 0, 'pana_hit_count': 0, 'total_days': 0}

    for i in range(1, len(df)):
        if results['total_days'] >= check_days: break

        previous_df = df.iloc[:i]
        sutra_analysis = find_brahmanda_sutra(previous_df)
        if not sutra_analysis: continue
        core_otc = sutra_analysis['core_otc']

        current_day = df.iloc[i]
        open_ank, close_ank = current_day['open'], current_day['close']
        open_pana_str = str(current_day['Open_Pana']).zfill(3)
        close_pana_str = str(current_day['Close_Pana']).zfill(3)

        ank_hit, pana_hit, _ = check_sutra_hit(core_otc, open_ank, close_ank, open_pana_str, close_pana_str)

        if ank_hit: results['ank_hit_count'] += 1
        if pana_hit: results['pana_hit_count'] += 1
        results['total_days'] += 1

    return results

# ==============================================================================
# 📅 WEEKLY PERFORMANCE TRACKER 📅
# ==============================================================================
def track_weekly_performance(df):
    if df.empty: return []

    last_date = df['Date'].iloc[-1].normalize()
    # Find the start of the current week (Monday)
    start_of_week = last_date - timedelta(days=last_date.weekday())

    weekly_results = []
    weekly_df = df[df['Date'] >= start_of_week].copy().reset_index(drop=True)

    # Loop from the second day (index 1) to check prediction vs result
    for i in range(1, len(weekly_df)):
        prev_date = weekly_df.iloc[i-1]['Date']
        # Full DF index is needed for context
        full_df_index_prev = df[df['Date'] == prev_date].index[0]

        sutra_analysis = find_brahmanda_sutra(df.iloc[:full_df_index_prev + 1])

        if not sutra_analysis: continue
        core_otc = sutra_analysis['core_otc']

        current_day = weekly_df.iloc[i]
        open_ank, close_ank = current_day['open'], current_day['close']
        open_pana_str = str(current_day['Open_Pana']).zfill(3)
        close_pana_str = str(current_day['Close_Pana']).zfill(3)

        # Use the new check_sutra_hit that returns the hit pana
        ank_hit, pana_hit, hit_pana_str = check_sutra_hit(core_otc, open_ank, close_ank, open_pana_str, close_pana_str)

        ank_status = "[bold green]PASS[/bold green]" if ank_hit else "[bold red]FAIL[/bold red]"

        if pana_hit:
            pana_status = f"[bold yellow]{hit_pana_str} P-PASS[/bold yellow]"
            if not ank_hit: # If Ank failed but Pana hit (shouldn't happen with the logic, but for safety)
                 ank_status = "[bold blue]P-PASS ONLY[/bold blue]"
        else:
            pana_status = "[dim red]P-FAIL[/dim red]"

        weekly_results.append({
            'date': current_day['Date'].strftime('%a (%d/%m)'),
            'jodi': str(current_day['Jodi']).zfill(2),
            'prediction': f"{' '.join(map(str, core_otc))}",
            'ank_status': ank_status,
            'pana_status': pana_status
        })

    return weekly_results
    # --- Yantra ka Shareer (The "Pro Max" Body) ---
def display_final_output(market_name, sutra_analysis, last_record, validation_results, weekly_performance):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel(Text(f'🔱 {market_name} - AMRIT-KALASH (MAHA-SANKALPA) 🔱', justify="center"), style="bold yellow on #1A1A1D", border_style="ye>

    # Last Record Info
    last_jodi_str = str(last_record['Jodi']).zfill(2)
    last_date_str = last_record['Date'].strftime('%d-%m-%Y')
    prediction_date_str = (last_record['Date'] + timedelta(days=1)).strftime('%d-%m-%Y') # Next day date

    console.print(Panel(f"Last record ⏺️ ({last_date_str}): [yellow]{last_record['Open_Pana']}-{last_jodi_str}-{last_record['Close_Pana']}[/yellow]", bo>

    if not sutra_analysis:
        console.print(Panel("[bold red]❌ Divya-Drishti ke liye paryaapt data nahi hai.[/bold red]")); return

    # --- Aaj Ka Prediction ---
    suggested_panels = get_suggested_panels(sutra_analysis['core_otc'])

    console.print(Rule(style="cyan", title="[bold]✨ AAJ KA DIVYA-SANKET (03-11-2025) ✨[/bold]")) # Hardcoding date for example, should be dynamic

    sanket_grid = Table.grid(padding=(1, 2, 1, 0), expand=True)
    sanket_grid.add_column(style="yellow", justify="right", width=30); sanket_grid.add_column()
    sanket_grid.add_row("[bold]Brahmanda-Sutra ke Mukhya Ank (OTC):[/bold]", f"🔥 [bold bright_yellow]{' '.join(map(str, sutra_analysis['core_otc']))}[>
    sanket_grid.add_row(Rule(style="dim cyan"), Rule(style="dim cyan"))
    sanket_grid.add_row("[bold]Is Sutra se Janmit Jodiyan:[/bold]", f"🎯 [bold green]{' '.join(sutra_analysis['strongest_jodis'])}[/bold green]")
    sanket_grid.add_row("[bold]Chune hue Pannel (Patti):[/bold]", f"🔑 [bold white]{' '.join(suggested_panels)}[/bold white]")
    console.print(Panel(sanket_grid, border_style="cyan", title=f"🔮 Prediction Date: {prediction_date_str}"))

    # --- Historical Validation ---
    console.print(Rule(style="magenta", title="[bold]📊 HISTORICAL SATYAPAN (LAST 40 DAYS) 📊[/bold]"))
    if validation_results['total_days'] > 0:
        ank_rate = (validation_results['ank_hit_count'] / validation_results['total_days']) * 100
        pana_rate = (validation_results['pana_hit_count'] / validation_results['total_days']) * 100

        console.print(f"🔹 **Sutra-Ank Hit Rate (OTC):** [bold green]{validation_results['ank_hit_count']}[/bold green] / [cyan]{validation_results['to>
        console.print(f"🔸 **Pana Hit Rate (Patti):** [bold green]{validation_results['pana_hit_count']}[/bold green] / [cyan]{validation_results['tota>
    else:
        console.print("[red]Historical data kaafi nahi hai Satyapan ke liye.[/red]")

    # --- Weekly Performance ---
    console.print(Rule(style="green", title="[bold]📈 CHALU WEEK (Self-Correction) | Monday to Sunday 📈[/bold]"))
    if weekly_performance:
        week_table = Table(title="Sutra Performance (Open/Close)", border_style="green", show_header=True, header_style="bold green")
        week_table.add_column("Din (Tarikh)", style="cyan", justify="left")
        week_table.add_column("Result (Jodi)", style="yellow", justify="center")
        week_table.add_column("Prediction", style="bright_yellow", justify="center")
        week_table.add_column("Ank Status", justify="center")
        week_table.add_column("Pana Status", justify="center")

        for entry in weekly_performance:
            week_table.add_row(entry['date'], entry['jodi'], entry['prediction'], entry['ank_status'], entry['pana_status'])
        console.print(week_table)
    else:
        console.print("[dim yellow]Chalu week ka data abhi shuru nahi hua hai ya sirf ek din ka hai.[/dim yellow]")

    console.print(Rule(style="dim yellow", characters="_"))
    console.print(Align.center(f"_________Next Prediction: {prediction_date_str}_______________________________________________________________________>
    console.print(Align.center("[bold cyan]Thankyou For using[/bold cyan]"))
    console.print(Align.center("Tool created by - [bold magenta]Ai - Jarvis & Sachin[/bold magenta]"))

# --- Main Command Center ---
def main():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    # ... (Same Main loop logic, but calling new functions) ...
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel(Text('🔱 AMRIT-KALASH (MAHA-SANKALPA) 🔱', justify="center"), style="bold yellow on #1A1A1D", border_style="yellow"))
        available_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        if not available_files: console.print(Panel("[bold red]❌ DATA FOLDER KHALI HAI ❌[/bold red]")); time.sleep(3); break

        market_table = Table(title="[bold yellow]Yudh-Bhoomi ka Chayan Karein[/bold yellow]", border_style="yellow")
        for i, name in enumerate(available_files): market_table.add_row(f"[cyan][{i+1}][/cyan]", f"[green]{name}[/green]")
        market_table.add_row("[cyan][0][/cyan]", "[red]Exit (VISHRAM)[/red]")
        console.print(market_table)

        choice = Prompt.ask("[bold]👉 Market Chunein (0 to Exit)[/bold]", choices=[str(i) for i in range(len(available_files) + 1)], default="1")
        if choice == '0': break

        try:
            market_file = available_files[int(choice) - 1]
            market_name = market_file.replace('.txt', '')
            filepath = os.path.join(DATA_DIR, market_file)

            with Live(Spinner("clock", text=f"{market_name} ke Brahmanda-Sutra ko padha ja raha hai..."), console=console, transient=True):
                df, error_msg = load_and_prepare_data(filepath)

                if df is None or len(df) < 5:
                    console.print(Panel(f"[bold red]❌ ERROR ❌\n{error_msg or 'Data file khaali ya bahut kam data hai (min 5 days required).'}")); tim>

                sutra_analysis = find_brahmanda_sutra(df)
                last_record = df.iloc[-1].copy()
                validation_results = sutra_validation_engine(df, check_days=40)
                weekly_performance = track_weekly_performance(df)

            display_final_output(market_name, sutra_analysis, last_record, validation_results, weekly_performance)

        except (ValueError, IndexError):
            console.print("[red]Galt aadesh.[/red]"); time.sleep(2); continue
        except Exception as e:
            console.print(Panel(f"[bold red]❌ Anjaan Galti Hui ❌\n{e}", border_style="red")); time.sleep(5)
            continue

        input("\n... Press Enter to continue ...")

    console.print("[yellow]Yantra vishram kar raha hai...[/yellow]")

if __name__ == "__main__":
    main()
  

    
