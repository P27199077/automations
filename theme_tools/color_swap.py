import re
file_path = "page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace slate- class colors with stone- class colors
content = content.replace("slate-950", "stone-950")
content = content.replace("slate-900", "stone-900")
content = content.replace("slate-850", "stone-850")
content = content.replace("slate-800", "stone-800")
content = content.replace("slate-700", "stone-700")
content = content.replace("slate-650", "stone-600")
content = content.replace("slate-600", "stone-600")
content = content.replace("slate-500", "stone-500")
content = content.replace("slate-450", "stone-400")
content = content.replace("slate-400", "stone-400")
content = content.replace("slate-355", "stone-400")
content = content.replace("slate-350", "stone-300")
content = content.replace("slate-300", "stone-300")
content = content.replace("slate-200", "stone-200")
content = content.replace("slate-100", "stone-100")

# 2. Replace ambient glows
content = content.replace("bg-cyan-500/10", "bg-amber-500/5")
content = content.replace("bg-purple-500/10", "bg-orange-500/5")
content = content.replace("cyan-500/15", "amber-500/10")
content = content.replace("cyan-500/20", "amber-500/15")
content = content.replace("purple-500/15", "orange-500/10")
content = content.replace("purple-500/20", "orange-500/15")
content = content.replace("cyan-950/20", "amber-950/30")
content = content.replace("cyan-950/35", "amber-950/45")
content = content.replace("cyan-900/30", "amber-900/40")
content = content.replace("cyan-900/35", "amber-900/45")
content = content.replace("purple-950/20", "orange-950/30")
content = content.replace("purple-950/35", "orange-950/45")
content = content.replace("purple-900/30", "orange-900/40")
content = content.replace("purple-900/35", "orange-900/45")
content = content.replace("cyan-950/40", "amber-950/30")
content = content.replace("cyan-950/50", "amber-950/30")
content = content.replace("purple-950/40", "orange-950/30")
content = content.replace("purple-950/50", "orange-950/30")

# 3. Replace text & background primary colors
content = content.replace("cyan-500", "amber-500")
content = content.replace("cyan-400", "amber-400")
content = content.replace("cyan-300", "amber-300")
content = content.replace("cyan-200", "amber-200")
content = content.replace("cyan-600", "amber-600")
content = content.replace("cyan-950", "amber-950")
content = content.replace("cyan-900", "amber-900")
content = content.replace("purple-500", "orange-500")
content = content.replace("purple-400", "orange-300")
content = content.replace("purple-300", "orange-300")
content = content.replace("purple-600", "orange-600")
content = content.replace("purple-950", "orange-950")
content = content.replace("purple-900", "orange-900")

# 4. Replace special gradients
content = content.replace("from-cyan-400 via-indigo-500 to-purple-500", "from-amber-200 via-stone-300 to-amber-600")
content = content.replace("from-cyan-400 to-purple-500", "from-amber-200 to-amber-600")
content = content.replace("from-cyan-400 via-indigo-400 to-purple-500", "from-amber-200 via-orange-300 to-amber-600")
content = content.replace("from-purple-600 to-purple-500", "from-orange-600 to-orange-500")
content = content.replace("from-cyan-500 to-cyan-600", "from-amber-500 to-amber-600")
content = content.replace("to-cyan-500", "to-amber-500")
content = content.replace("to-cyan-600", "to-amber-600")
content = content.replace("from-purple-500", "from-orange-500")
content = content.replace("to-purple-500", "to-orange-500")

# Let's write the modified file back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Color re-theme completed successfully.")
