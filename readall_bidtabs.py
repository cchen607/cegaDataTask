import fitz  # PyMuPDF

input_pdf = "Bid Tabs 2018.pdf"
output_pdf = "bidtabs.pdf"

doc = fitz.open(input_pdf)
new_doc = fitz.open()

seen_projects = set()

for page in doc:
    text = page.get_text()
    for line in text.splitlines():
        if line.strip().startswith("Project No."):
            project_no = line.strip().split()[-1]
            if project_no not in seen_projects:
                seen_projects.add(project_no)
                new_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)
            break  # Stop once project is found

new_doc.save(output_pdf) # Save shortened PDF
new_doc.close()
doc = fitz.open(output_pdf)
full_text = "\n".join([page.get_text() for page in doc])

# Make blocks by pages with "Project No."
project_blocks = re.split(r"\n(?=Project No\.\s+\d+)", full_text)

# Contain all project results
all_projects = []

for block in project_blocks:
    # Extract project_id (PID)
    project_id = re.search(r"PID\s+(\d+)", block)
    project_id = project_id.group(1) if project_id else "NA"
    # Engineer's estimate
    eng_estimate = re.search(r"Engineer.?s Estimate:\s*\$([\d,]+\.\d{2})", block)
    eng_estimate = eng_estimate.group(1) if eng_estimate else "NA"
    # Award amount
    award_amount = re.search(r"Award Amount:\s*\$([\d,]+\.\d{2})", block)
    award_amount = award_amount.group(1) if award_amount else "NA"
    # Bidder names
    bidder_blocks = re.findall(r"(.*?)\nBidder \d", block, re.DOTALL)
    bid_names = []
    for section in bidder_blocks:
        lines = section.strip().split("\n")
        for line in lines:
            line = line.strip() # Need to specifically look for these words
            if line.isupper() and re.search(r"(COMPANY|INC|LLC|CORP|CONSTRUCTION)", line): 
                bid_names.append(line)
                break  # Only take first match per block

    # Record results
    all_projects.append({
        'project_id': project_id,
        'eng_estimate': eng_estimate,
        'win_bid': award_amount,
        'num_bidders': len(bid_names),
        'bidders_list': bid_names
    })

# Create DataFrame and export
df = pd.DataFrame(all_projects)
print(df)
df.to_excel("project_bids.xlsx", index=False)