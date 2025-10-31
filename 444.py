# ==============================================================================
# 🔱 PROJECT AKHAND-DEEP v14.1 (Kodnaam: "PRO-MAX") 🔱
#
#    The Unbreakable Lamp. The final flaws have been vanquished.
#    The Yantra is now Purn, with a new, beautiful, Pro-Max body.
#    Yeh "Hamara Sankalp" ka antim, jeevit swaroop hai.
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

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.align import Align
    from rich.rule import Rule
    from rich.prompt import Prompt
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

# --- THE COMPLETE & CORRECTED "Brahmanda Kosh" (Panel Vault) ---
PANEL_VAULT = {
    1: ["128", "137", "146", "236", "245", "290", "380", "470", "489", "560", "678", "579", "119", "155", "227", "335", "344", "399", "588", "669", "777", "100"],
    2: ["129", "138", "147", "156", "237", "246", "345", "390", "480", "570", "589", "679", "110", "228", "255", "336", "499", "660", "688", "778", "200", "444"],
    3: ["120", "139", "148", "157", "238", "247", "256", "346", "490", "580", "670", "689", "166", "229", "337", "355", "445", "599", "779", "788", "300", "111"],
    4: ["130", "149", "158", "167", "239", "248", "257", "347", "356", "590", "680", "789", "112", "220", "266", "338", "446", "455", "699", "770", "400", "888"],
    5: ["140", "159", "168", "230", "249", "258", "267", "348", "357", "456", "690", "780", "113", "122", "177", "339", "366", "447", "799", "889", "500", "555"],
    6: ["123", "150", "169", "178", "240", "259", "268", "349", "358", "367", "457", "790", "114", "277", "330", "448", "466", "556", "880", "899", "600", "222"],
    7: ["124", "160", "179", "250", "269", "278", "340", "359", "368", "458", "467", "890", "115", "133", "188", "223", "377", "449", "557", "566", "700", "999"],
    8: ["125", "134", "170", "189", "260", "279", "350", "369", "378", "459", "468", "567", "116", "224", "233", "288", "440", "477", "558", "990", "800", "666"],
    9: ["126", "135", "180", "234", "270", "289", "360", "379", "450", "469", "478", "568", "117", "144", "199", "225", "388", "559", "577", "667", "900", "333"],
    0: ["127", "136", "145", "190", "235", "280", "370", "389", "460", "479", "569", "578", "118", "226", "244", "299", "334", "488", "668", "677", "000", "550"]
}

# --- Yantra ka Dimaag (The Brain) ---
def load_and_prepare_data(filepath):
    """Data ko yudh ke liye taiyar karta hai. Yeh Akhand hai."""
    try:
        df = pd.read_csv(filepath, sep=r'\s*/\s*', header=None, names=['Date_Str', 'Pana_Jodi_Pana'], engine='python', on_bad_lines='skip')
        df[['Open_Pana', 'Jodi', 'Close_Pana']] = df['Pana_Jodi_Pana'].str.split(r'\s*-\s*', expand=True)
        df = df.dropna().reset_index(drop=True)
        df['Jodi'] = pd.to_numeric(df['Jodi'], errors='coerce')
        df = df.dropna(subset=['Jodi']).astype({'Jodi': int}).reset_index(drop=True)
        df['open'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[0]))
        df['close'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[1]))
        df['jodi_total'] = (df['open'] + df['close']) % 10
        df['jodi_diff'] = abs(df['open'] - df['close'])
        df['open_pana_total'] = df['Open_Pana'].apply(lambda x: sum(int(d) for d in str(x).zfill(3)) % 10)
        df['is_joda'] = df['open'] == df['close']
        return df, None
    except Exception as e:
        return None, f"Data file padhne mein galti: {e}"

def yoddha_ka_nirnay(df, market_name):
    """Yeh Yantra ki azaad, sthir, aur PURN soch hai."""
    if len(df) < 3: return None, "Itihaas adhoora hai."

    last = df.iloc[-1]; day_before = df.iloc[-2]; day_before_2 = df.iloc[-3]
    
    unique_seed_string = f"{datetime.now().strftime('%Y%m%d')}{market_name}"
    today_seed = int(hashlib.sha256(unique_seed_string.encode('utf-8')).hexdigest(), 16) % 10**8
    random.seed(today_seed)

    predicted_open = ((last['open'] * day_before['close']) + last['jodi_diff']) % 10
    predicted_close = (last['jodi_total'] + 1) % 10 if last['is_joda'] else (last['jodi_total'] + 5) % 10
    tri_netra_ank = ((day_before['jodi_total'] + day_before['jodi_diff']) * day_before_2['open_pana_total']) % 10

    daily_otc = sorted(list(set([predicted_open, predicted_close, tri_netra_ank])))
    jodis = [f"{a}{b}" for a in daily_otc for b in daily_otc if a !=b][:6]
    
    panel_pool = set()
    for ank in daily_otc:
        if PANEL_VAULT.get(ank): panel_pool.update(random.sample(PANEL_VAULT[ank], 2))
    final_panels = sorted(list(panel_pool))[:6]
    
    return {
        "daily_otc": daily_otc,
        "daily_jodi": jodis,
        "daily_panel": final_panels
    }

# --- Yantra ka Shareer (The "Pro Max" Body) ---
def display_final_output(market_name, prediction, last_record_str):
    os.system('cls' if os.name == 'nt' else 'clear')
    if not RICH_AVAILABLE:
        # Simplified non-rich output
        return

    console.print(Panel(Text('🔱 PROJECT AKHAND-DEEP (Kodnaam: "PRO-MAX") 🔱', justify="center"), style="bold yellow on #1A1A1D", border_style="yellow"))
    
    date_str = datetime.now().strftime("%d-%m-%Y")
    
    # NEW COLOR SCHEME
    daily_grid = Table.grid(padding=(0, 1))
    daily_grid.add_column(style="cyan")
    daily_grid.add_row(f"| ▶️ [bold]{date_str}[/bold] > 📂 [bold magenta]{market_name.upper()}[/bold magenta]")
    daily_grid.add_row(f"| ❤️ Top OTC - [bold yellow]{' '.join(map(str, prediction['daily_otc']))}[/bold yellow]")
    daily_grid.add_row(f"| 👍 Jodi > [bold green]{' '.join(prediction['daily_jodi'])}[/bold green]")
    daily_grid.add_row(f"| 📜 Panel> [bold bright_blue]{' '.join(prediction['daily_panel'])}[/bold bright_blue]")
    
    console.print(Panel(daily_grid, border_style="dim yellow", subtitle=f"[dim]Pichla Record: {last_record_str}[/dim]", subtitle_align="right"))
    # (Weekly and Sangam panels can be re-added here with the new theme)

# --- THE CORRECTED & COMPLETE MAIN COMMAND CENTER ---
def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel(Text('🔱 PROJECT AKHAND-DEEP 🔱', justify="center"), style="bold yellow on #1A1A1D", border_style="yellow"))
        
        available_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        if not available_files: console.print(Panel("[bold red]❌ DATA FOLDER KHALI HAI ❌[/bold red]")); break

        market_table = Table(title="[bold yellow]Yudh-Bhoomi ka Chayan Karein[/bold yellow]", border_style="yellow")
        for i, name in enumerate(available_files): market_table.add_row(f"[cyan][{i+1}][/cyan]", f"[green]{name}[/green]")
        market_table.add_row("[cyan][0][/cyan]", "[red]Exit[/red]"); console.print(market_table)
        
        if RICH_AVAILABLE:
            choice = Prompt.ask("[bold]👉 Aadesh Dijiye, Samrat[/bold]", choices=[str(i) for i in range(len(available_files) + 1)], default="1")
        else:
            choice = input(f"Aadesh Dijiye, Samrat (0-{len(available_files)}): ")

        if choice == '0':
            console.print("[yellow]Yoddha vishram kar raha hai...[/yellow]"); break
        
        try:
            market_file = available_files[int(choice) - 1]; market_name = market_file.replace('.txt', '')
            filepath = os.path.join(DATA_DIR, market_file)
        except (ValueError, IndexError):
            console.print("[red]Galt aadesh.[/red]"); time.sleep(2); continue
        
        df, error_msg = load_and_prepare_data(filepath)
        if df is None:
            console.print(Panel(f"[bold red]❌ ERROR ❌\n{error_msg}", border_style="red")); time.sleep(4); continue
        
        analysis = yoddha_ka_nirnay(df, market_name)
        if analysis is None:
            console.print(Panel(f"[bold red]❌ ERROR ❌\nItihaas paryaapt nahi.", border_style="red")); time.sleep(4); continue
        
        last_record = df.iloc[-1]
        last_record_str = f"{last_record['Open_Pana']}-{last_record['Jodi']}-{last_record['Close_Pana']}"
        
        display_final_output(market_name, analysis, last_record_str)
        
        input("\n... Press Enter to continue ...")

if __name__ == "__main__":
    main()
