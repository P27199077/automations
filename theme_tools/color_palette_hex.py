import re

file_path = "/Users/tanishagupta/Desktop/bartr-web/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Helper list of direct replacements
replacements = [
    # 1. Page backgrounds
    ("bg-stone-950", "bg-[#18110b]"), # Extra dark coffee body background
    ("bg-stone-900/90", "bg-[#3B2415]/90"), # Main nav bar bg
    ("bg-stone-900/80", "bg-[#3B2415]/80"), 
    ("bg-stone-900/60", "bg-[#3B2415]/60"), # Cards
    ("bg-stone-900/50", "bg-[#3B2415]/50"), 
    ("bg-stone-900/40", "bg-[#3B2415]/40"), 
    ("bg-stone-900/30", "bg-[#3B2415]/30"), 
    ("bg-stone-900/20", "bg-[#3B2415]/20"), 
    ("bg-stone-900", "bg-[#3B2415]"), 
    ("bg-stone-955/60", "bg-[#3B2415]/60"),
    ("bg-stone-950/60", "bg-[#18110b]/60"),
    ("bg-stone-950/40", "bg-[#18110b]/40"),
    ("bg-stone-950/20", "bg-[#18110b]/20"),
    ("bg-stone-950/70", "bg-[#18110b]/70"),
    ("bg-stone-950/80", "bg-[#18110b]/80"),
    ("bg-stone-950/95", "bg-[#18110b]/95"),
    ("bg-stone-950", "bg-[#18110b]"),
    ("from-stone-900 to-stone-800", "from-[#3B2415] to-[#693F26]"),
    ("border-stone-900/30", "border-[#693F26]/30"),
    ("border-stone-900/35", "border-[#693F26]/35"),
    ("border-stone-950", "border-[#18110b]"),

    # 2. Page borders
    ("border-stone-800/80", "border-[#693F26]/40"),
    ("border-stone-800/60", "border-[#693F26]/30"),
    ("border-stone-800/30", "border-[#693F26]/20"),
    ("border-stone-800", "border-[#693F26]/40"),
    ("border-stone-700/60", "border-[#693F26]/50"),
    ("border-stone-700", "border-[#693F26]/50"),
    ("hover:border-stone-700", "hover:border-[#A26F25]/40"),
    ("hover:border-stone-800", "hover:border-[#693F26]/50"),
    ("border-r border-stone-800", "border-r border-[#693F26]/30"),
    ("border-b border-stone-800", "border-b border-[#693F26]/30"),
    ("border-t border-stone-800", "border-t border-[#693F26]/30"),
    ("border-t border-stone-800/50", "border-t border-[#693F26]/30"),
    ("border-t border-stone-800/80", "border-t border-[#693F26]/40"),

    # 3. Ambient Glows
    ("bg-amber-500/5", "bg-[#A26F25]/10"),
    ("bg-orange-500/5", "bg-[#693F26]/10"),
    ("bg-amber-500/10", "bg-[#A26F25]/15"),
    ("bg-orange-500/10", "bg-[#693F26]/15"),
    
    # 4. Text & Accent colors
    ("text-stone-100", "text-[#ECD8B1]"), # Cream primary text
    ("text-stone-200", "text-[#ECD8B1]"),
    ("text-stone-300", "text-[#D5C2A5]"), # Beige secondary text
    ("text-stone-400", "text-[#D5C2A5]"), 
    ("text-stone-500", "text-[#D5C2A5]/70"),
    ("text-stone-600", "text-[#693F26]"),
    ("text-stone-650", "text-[#693F26]"),
    ("text-amber-400", "text-[#A26F25]"), # Golden Ochre for highlights
    ("text-amber-300", "text-[#ECD8B1]"),
    ("text-orange-300", "text-[#D5C2A5]"),
    ("text-rose-500", "text-[#c2410c]"), # Warm clay/terracotta for nope
    ("hover:text-rose-350", "hover:text-[#c2410c]"),
    ("text-cyan-400", "text-[#A26F25]"),
    ("text-cyan-300", "text-[#D5C2A5]"),
    ("bg-cyan-500", "bg-[#A26F25]"),
    ("hover:bg-cyan-600", "hover:bg-[#693F26]"),

    # 5. Buttons & Badges (Arb values)
    ("bg-amber-500/15 border-amber-500/20 text-amber-400 font-bold", "bg-[#A26F25]/20 border-[#A26F25]/30 text-[#ECD8B1] font-bold"),
    ("bg-[#A26F25]/20 border-[#A26F25]/30 text-[#ECD8B1] font-bold", "bg-[#A26F25]/20 border-[#A26F25]/30 text-[#ECD8B1] font-bold"),
    ("border-purple-500 bg-purple-500/15 text-purple-300", "border-[#693F26] bg-[#693F26]/20 text-[#D5C2A5]"),
    ("bg-[#A26F25]/15 border-[#A26F25]/25 text-[#ECD8B1]", "bg-[#A26F25]/15 border-[#A26F25]/25 text-[#ECD8B1]"),
    ("bg-[#A26F25]/15 border-[#A26F25]/25 text-[#ECD8B1] font-bold", "bg-[#A26F25]/15 border-[#A26F25]/25 text-[#ECD8B1] font-bold"),
    ("bg-amber-500 hover:bg-amber-600 text-stone-950", "bg-[#A26F25] hover:bg-[#693F26] text-[#ECD8B1]"),
    ("bg-amber-600 hover:bg-amber-700 text-stone-950", "bg-[#A26F25] hover:bg-[#693F26] text-[#ECD8B1]"),
    ("bg-gradient-to-tr from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-stone-950", "bg-gradient-to-tr from-[#A26F25] to-[#693F26] hover:from-[#A26F25]/80 hover:to-[#693F26]/80 text-[#ECD8B1]"),
    ("bg-gradient-to-tr from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950", "bg-gradient-to-tr from-[#A26F25] to-[#693F26] hover:from-[#A26F25]/80 hover:to-[#693F26]/80 text-[#ECD8B1]"),
    ("bg-gradient-to-tr from-cyan-500 to-cyan-600 hover:from-cyan-400 hover:to-cyan-500 text-slate-950", "bg-gradient-to-tr from-[#A26F25] to-[#693F26] hover:from-[#A26F25]/80 hover:to-[#693F26]/80 text-[#ECD8B1]"),
    ("bg-amber-950/30 text-amber-200 border-amber-900/40", "bg-[#A26F25]/20 text-[#ECD8B1] border-[#A26F25]/30"),
    ("bg-orange-950/30 text-orange-200 border-orange-905/40", "bg-[#693F26]/20 text-[#D5C2A5] border-[#693F26]/30"),
    ("bg-amber-950/40 text-amber-200 border-amber-900/35", "bg-[#A26F25]/15 text-[#ECD8B1] border-[#A26F25]/25"),
    ("bg-orange-950/40 text-orange-200 border-orange-900/35", "bg-[#693F26]/15 text-[#D5C2A5] border-[#693F26]/25"),
    ("bg-amber-950/50 text-amber-400 border-amber-900/30", "bg-[#A26F25]/15 text-[#ECD8B1] border-[#A26F25]/25"),
    ("bg-orange-950/50 text-orange-400 border-orange-900/30", "bg-[#693F26]/15 text-[#D5C2A5] border-[#693F26]/25"),
    ("text-slate-950", "text-[#3B2415]"),
    ("text-stone-950", "text-[#3B2415]"),
    ("text-slate-650", "text-[#693F26]"),
    ("text-slate-700", "text-[#693F26]"),
    ("text-slate-500", "text-[#D5C2A5]"),
    ("text-slate-400", "text-[#D5C2A5]"),
    ("text-slate-300", "text-[#D5C2A5]"),
    ("text-slate-200", "text-[#ECD8B1]"),
    ("border-slate-800", "border-[#693F26]/40"),
    ("border-slate-700", "border-[#693F26]/50"),

    # 6. Gradients re-themes
    ("from-amber-200 via-stone-300 to-amber-600", "from-[#ECD8B1] via-[#D5C2A5] to-[#A26F25]"),
    ("from-amber-200 via-orange-300 to-amber-600", "from-[#ECD8B1] via-[#A26F25] to-[#693F26]"),
    ("from-amber-200 to-amber-600", "from-[#ECD8B1] to-[#A26F25]"),
    ("from-orange-600 to-orange-500", "from-[#693F26] to-[#A26F25]"),
    ("from-amber-500 to-amber-600", "from-[#A26F25] to-[#693F26]"),
    ("to-amber-500", "to-[#A26F25]"),
    ("to-amber-600", "to-[#693F26]"),
    ("from-orange-500", "from-[#693F26]"),
    ("to-orange-500", "to-[#A26F25]"),
    ("from-cyan-500 to-cyan-600", "from-[#A26F25] to-[#693F26]"),
    ("from-cyan-400 to-purple-500", "from-[#ECD8B1] to-[#A26F25]"),
    ("from-cyan-400 via-indigo-500 to-purple-500", "from-[#ECD8B1] via-[#D5C2A5] to-[#A26F25]"),
    ("bg-gradient-to-tr from-cyan-500 to-purple-600", "bg-gradient-to-tr from-[#A26F25] to-[#693F26]"),

    # 7. Map pin previews
    ("text-cyan-400", "text-[#A26F25]"),
    ("bg-cyan-400", "bg-[#A26F25]"),
    ("bg-cyan-950", "bg-[#3B2415]"),
    ("border-cyan-800", "border-[#A26F25]/40"),
    ("bg-purple-950", "bg-[#3B2415]"),
    ("border-purple-800", "border-[#693F26]/40"),
    ("bg-cyan-950/20", "bg-[#A26F25]/10"),
    ("bg-purple-950/20", "bg-[#693F26]/10"),
    ("bg-cyan-950/60", "bg-[#A26F25]/20"),
    ("bg-purple-950/60", "bg-[#693F26]/20"),
    ("border-cyan-900/30", "border-[#A26F25]/30"),
    ("border-purple-900/30", "border-[#693F26]/30"),
    ("border-cyan-900/35", "border-[#A26F25]/35"),
    ("border-purple-900/35", "border-[#693F26]/35"),
    ("text-cyan-500", "text-[#A26F25]"),
    ("text-purple-500", "text-[#693F26]"),
    ("text-amber-500", "text-[#D5C2A5]"),
    ("text-emerald-500", "text-[#ECD8B1]"),
]

for target, replacement in replacements:
    content = content.replace(target, replacement)

# Direct map rendering pin colors
content = content.replace("pin.category === 'study' ? 'text-amber-500' :", "pin.category === 'study' ? 'text-[#A26F25]' :")
content = content.replace("pin.category === 'music' ? 'text-orange-500' :", "pin.category === 'music' ? 'text-[#693F26]' :")
content = content.replace("pin.category === 'activity' ? 'text-amber-500' :", "pin.category === 'activity' ? 'text-[#D5C2A5]' :")
content = content.replace("'text-emerald-500';", "'text-[#ECD8B1]';")

content = content.replace("pin.category === 'study' ? 'bg-amber-400' :", "pin.category === 'study' ? 'bg-[#A26F25]' :")
content = content.replace("pin.category === 'music' ? 'bg-orange-500' :", "pin.category === 'music' ? 'bg-[#693F26]' :")
content = content.replace("pin.category === 'activity' ? 'bg-amber-500' :", "pin.category === 'activity' ? 'bg-[#D5C2A5]' :")
content = content.replace("'bg-emerald-500';", "'bg-[#ECD8B1]';")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Exact hex color theme completed successfully.")
