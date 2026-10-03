"""
Static testimonies data for David Sudher Ministries.
Clearly marked sample content until replaced by the owner.
"""

TESTIMONIES = [
    {
        "slug": "sample-family-restoration",
        "name": "Priya R. (Sample)",
        "location": "Bangalore, India",
        "title": "Restoration and Peace in Our Family",
        "category": "family",
        "excerpt": "A sample testimony showing how God answered persistent prayer and brought lasting peace and reconciliation to our home.",
        "story": "This is sample testimony content for layout preview. God restored our family in ways only He could. Through persistent prayer, grace, and spiritual guidance, we witnessed reconciliation and a new foundation of love and peace established in our household.",
        "photo": "/static/ministry/images/prayer-community.jpg",
        "featured": True,
    },
    {
        "slug": "sample-clarity-calling",
        "name": "Daniel K. (Sample)",
        "location": "Hyderabad, India",
        "title": "Finding Purpose and Boldness in Christ",
        "category": "calling",
        "excerpt": "A sample testimony reflecting how mentoring and prayer helped clarify calling and instill confidence in God's plan.",
        "story": "This is sample testimony content for layout preview. For years I felt uncertain about my future. Attending a ministry gathering and receiving prayer brought clarity to my life's assignment and courage to step out in faith and serve.",
        "photo": "/static/ministry/images/prayer-young-man.jpg",
        "featured": False,
    },
    {
        "slug": "sample-healing-touch",
        "name": "Sarah M. (Sample)",
        "location": "United States",
        "title": "God's Grace and Restoring Touch",
        "category": "healing",
        "excerpt": "A sample testimony representing physical and emotional healing through prayer and steadfast trust in God's promises.",
        "story": "This is sample testimony content for layout preview. In the midst of illness and physical fatigue, believers stood with me in prayer. God brought strength, complete recovery, and renewed faith that His power is alive today.",
        "photo": "",
        "featured": False,
    },
    {
        "slug": "sample-provision-faithfulness",
        "name": "Marcus E. (Sample)",
        "location": "Pakistan",
        "title": "Faithful Provision in a Season of Need",
        "category": "provision",
        "excerpt": "A sample testimony illustrating God opening unexpected doors when circumstances seemed entirely impossible.",
        "story": "This is sample testimony content for layout preview. During a season of urgent financial need and uncertainty, we chose to trust God's Word. Miraculously, provision arrived right on time through unexpected avenues.",
        "photo": "",
        "featured": False,
    },
]

CATEGORY_LABELS = {
    "salvation": "Salvation",
    "healing": "Healing",
    "provision": "Provision",
    "family": "Family",
    "calling": "Calling",
    "deliverance": "Deliverance",
}

for item in TESTIMONIES:
    item["category_display"] = CATEGORY_LABELS.get(item["category"], item["category"].capitalize())
    clean_name = item["name"].replace("(Sample)", "").strip()
    item["initials"] = clean_name[0] if clean_name else "T"
