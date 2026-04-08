import pdfplumber
import os

pdf_dir = r"C:\Users\elgin\Documents\GitHub\IS431\md_uploads\Human_Proportions\Academic Publications"

# Pages likely to contain landmark height tables in Bodyspace
# Based on TOC: Chapter 2 (Body Dimensions ~p47), Chapter 3 (Human Diversity ~p55)
# Relevant pages from extraction were spread widely - look at specific ones

target_pages_bodyspace = list(range(36, 60)) + list(range(73, 100))
target_pages_pilots = list(range(5, 15))

def extract_pages(filename, target_pages, out_file):
    path = os.path.join(pdf_dir, filename)
    results = []
    with pdfplumber.open(path) as pdf:
        total = len(pdf.pages)
        print(f"{filename}: {total} pages total")
        for i in target_pages:
            if i <= total:
                page = pdf.pages[i-1]
                text = page.extract_text() or ""
                # Also try to extract tables
                tables = page.extract_tables()
                results.append(f"\n{'='*50}\nPAGE {i}\n{'='*50}\n{text}")
                if tables:
                    results.append(f"\n[TABLES ON PAGE {i}]:")
                    for t in tables:
                        for row in t:
                            results.append(" | ".join([str(c) if c else "" for c in row]))
    with open(out_file, "w", encoding="utf-8", errors="replace") as f:
        f.write("\n".join(results))
    print(f"Saved to {out_file}")

extract_pages(
    "Bodyspace_26_04_08_16_00_15.pdf",
    target_pages_bodyspace,
    r"C:\Users\elgin\Documents\GitHub\IS431\md_uploads\Human_Proportions\bodyspace_landmark_pages.txt"
)

extract_pages(
    "Anthropometry of Brazilian Air Force pilots.pdf",
    target_pages_pilots,
    r"C:\Users\elgin\Documents\GitHub\IS431\md_uploads\Human_Proportions\pilots_data_pages.txt"
)
