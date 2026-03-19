import os

ui_src_dir = '/Users/shreyas/rice_research/RiceResearchFinder/ui/src'

for root, _, files in os.walk(ui_src_dir):
    for file in files:
        if file.endswith(('.js', '.jsx')):
            filepath = os.path.join(root, file)
            # Skip About.jsx since it was deleted
            if file == 'About.jsx':
                continue
            with open(filepath, 'r') as f:
                content = f.read()
            
            new_content = content
            # Order matters: replace Texas A&M first, TAMU next, tamu next, Aggies next, Aggie next
            new_content = new_content.replace('Texas A&M', 'Rice')
            new_content = new_content.replace('Texas A&amp;M', 'Rice')
            new_content = new_content.replace('TAMU', 'Rice')
            new_content = new_content.replace('tamu', 'rice')
            new_content = new_content.replace('Aggies', 'Owls')
            new_content = new_content.replace('Aggie', 'Owl')
            new_content = new_content.replace('maroon', 'riceblue')
            new_content = new_content.replace('cream', 'ricewhite')
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated {os.path.relpath(filepath, ui_src_dir)}")
