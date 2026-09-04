#!/usr/bin/env python3
"""Track 2C — Africa + Middle East + Asia-Pacific exhaustive research apply.

Updates jurisdiction registry, source register, atlas deep maps, regional slices,
and coverage report for PR #7 Track 2C. Honest gaps only; no fabricated EXACT maps.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STANDARDS = ROOT / "kids" / "standards"
REVIEWED = "2026-09-03"
DISCLAIMER = (
    "Editorial crosswalk only; not a certification or authority endorsement claim."
)

# ---------------------------------------------------------------------------
# Jurisdiction research (AFR / ME / APAC). Status never left NOT_YET if researched.
# ---------------------------------------------------------------------------

JUR_RESEARCH: dict[str, dict] = {
    # --- Africa (was NOT_YET or deepen) ---
    "JUR-DZ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Algeria)",
        "notes": "National education programmes via MEN portal; Arabic/French primary — TRANSLATION_REQUIRED for depth.",
    },
    "JUR-AO": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministério da Educação (Angola)",
        "notes": "National basic education curriculum instruments via MED; Portuguese primary — TRANSLATION_REQUIRED.",
    },
    "JUR-BJ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère des Enseignements Maternel et Primaire (Benin)",
        "notes": "Francophone programmes scolaires identified at ministry level; TRANSLATION_REQUIRED.",
    },
    "JUR-BW": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Skills Development (Botswana)",
        "notes": "National curriculum / outcomes-based instruments identified via MoE; deeper PDF pins pending.",
    },
    "JUR-BF": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Burkina Faso)",
        "notes": "Francophone curricula; TRANSLATION_REQUIRED for clause work.",
    },
    "JUR-BI": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale et de la Recherche scientifique (Burundi)",
        "notes": "National programmes; French/Kirundi primary — TRANSLATION_REQUIRED.",
    },
    "JUR-CV": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministério da Educação (Cabo Verde)",
        "notes": "Portuguese-language national curriculum; TRANSLATION_REQUIRED.",
    },
    "JUR-CM": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère des Enseignements Secondaires / Basic Education (Cameroon)",
        "notes": "Bilingual (EN/FR) system; deep mapping needs language-specific pins — TRANSLATION_REQUIRED for FR streams.",
    },
    "JUR-CF": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Central African Republic)",
        "notes": "Francophone programmes; public portal depth limited — TRANSLATION_REQUIRED.",
    },
    "JUR-TD": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Chad)",
        "notes": "Francophone/Arabic system; TRANSLATION_REQUIRED.",
    },
    "JUR-KM": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Comoros)",
        "notes": "Francophone/Arabic curricula; TRANSLATION_REQUIRED.",
    },
    "JUR-CG": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Enseignement primaire, secondaire et de l'Alphabétisation (Congo)",
        "notes": "Francophone programmes; TRANSLATION_REQUIRED.",
    },
    "JUR-CD": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Enseignement primaire, secondaire et technique (DRC)",
        "notes": "National programmes scolaires; French primary — TRANSLATION_REQUIRED; portal stability variable.",
    },
    "JUR-CI": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale et de l'Alphabétisation (Côte d'Ivoire)",
        "notes": "Francophone curricula / SOE; TRANSLATION_REQUIRED.",
    },
    "JUR-DJ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale et de la Formation professionnelle (Djibouti)",
        "notes": "Francophone/Arabic system; TRANSLATION_REQUIRED.",
    },
    "JUR-GQ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministerio de Educación (Equatorial Guinea)",
        "notes": "Spanish/French system; TRANSLATION_REQUIRED; limited public English sources.",
    },
    "JUR-ER": {
        "research_status": "ACCESS_BLOCKED",
        "education_authority": "Ministry of Education (Eritrea)",
        "notes": "Official curriculum documents not reliably available via open public portals at research time.",
    },
    "JUR-SZ": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Training (Eswatini)",
        "notes": "National curriculum instruments identified via MoET; deeper PDF edition pins pending.",
    },
    "JUR-ET": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Ethiopia)",
        "framework_ids": ["FW-ET-CURRICULUM-FRAMEWORK"],
        "notes": "Curriculum Framework for Ethiopian Education (KG–Grade 12) retrieved via moe.gov.et; Amharic depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-GA": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Gabon)",
        "notes": "Francophone programmes; TRANSLATION_REQUIRED.",
    },
    "JUR-GM": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Basic and Secondary Education (The Gambia)",
        "notes": "National curriculum / syllabus instruments identified; deeper mapping pending.",
    },
    "JUR-GN": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale et de l'Alphabétisation (Guinea)",
        "notes": "Francophone curricula; TRANSLATION_REQUIRED.",
    },
    "JUR-GW": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministério da Educação Nacional (Guinea-Bissau)",
        "notes": "Portuguese-language system; TRANSLATION_REQUIRED; limited portal depth.",
    },
    "JUR-LS": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Training (Lesotho)",
        "notes": "National curriculum instruments identified; deeper PDF pins pending.",
    },
    "JUR-LR": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Liberia)",
        "notes": "National curriculum / early grade instruments identified at ministry level.",
    },
    "JUR-LY": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Libya)",
        "notes": "Arabic national programmes; TRANSLATION_REQUIRED; portal access variable.",
    },
    "JUR-MG": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Madagascar)",
        "notes": "Francophone/Malagasy curricula; TRANSLATION_REQUIRED.",
    },
    "JUR-MW": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Malawi)",
        "notes": "Primary curriculum / syllabus instruments identified via MoE; deeper mapping pending.",
    },
    "JUR-ML": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Mali)",
        "notes": "Francophone curricula; TRANSLATION_REQUIRED.",
    },
    "JUR-MR": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Mauritania)",
        "notes": "Arabic/French system; TRANSLATION_REQUIRED.",
    },
    "JUR-MU": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education, Tertiary Education, Science and Technology (Mauritius)",
        "notes": "National Curriculum Framework / primary instruments identified via MoE portal.",
    },
    "JUR-MA": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale, du Préscolaire et des Sports (Morocco)",
        "notes": "Framework Law 51.17 reform / programmes; Arabic/French primary — TRANSLATION_REQUIRED.",
    },
    "JUR-MZ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministério da Educação e Desenvolvimento Humano (Mozambique)",
        "notes": "Portuguese national curriculum; TRANSLATION_REQUIRED.",
    },
    "JUR-NA": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education, Arts and Culture (Namibia)",
        "notes": "National Curriculum for Basic Education identified; deeper subject pins pending.",
    },
    "JUR-NE": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Niger)",
        "notes": "Francophone programmes; TRANSLATION_REQUIRED.",
    },
    "JUR-RW": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education / Rwanda Education Board (REB)",
        "framework_ids": ["FW-RW-CBC"],
        "notes": "Competence-based Curriculum Framework identified via REB/MoE; deep mapping pending.",
    },
    "JUR-ST": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministério da Educação e Ensino Superior (Sao Tome and Principe)",
        "notes": "Portuguese-language curricula; TRANSLATION_REQUIRED; limited portal depth.",
    },
    "JUR-SN": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation nationale (Senegal)",
        "notes": "Francophone programmes / curricula; TRANSLATION_REQUIRED.",
    },
    "JUR-SC": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Seychelles)",
        "notes": "National Curriculum Framework identified; deeper PDF pins pending.",
    },
    "JUR-SL": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Basic and Senior Secondary Education (Sierra Leone)",
        "notes": "National curriculum / early grade instruments identified; deeper mapping pending.",
    },
    "JUR-SO": {
        "research_status": "ACCESS_BLOCKED",
        "education_authority": "Federal Ministry of Education (Somalia) / member-state authorities",
        "notes": "Fragmented federal/member-state systems; stable national early-years/primary PDF corpus not reliably open-access.",
    },
    "JUR-SS": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of General Education and Instruction (South Sudan)",
        "notes": "National curriculum instruments identified at high level; deeper PDF edition pins pending; access can be intermittent.",
    },
    "JUR-SD": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Sudan)",
        "notes": "Arabic national programmes; TRANSLATION_REQUIRED; portal access variable amid conflict.",
    },
    "JUR-TZ": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education, Science and Technology / TIE (Tanzania)",
        "notes": "Competence-based curriculum reform instruments identified; Swahili depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-TG": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère des Enseignements primaire, secondaire, technique et de l'Artisanat (Togo)",
        "notes": "Francophone programmes; TRANSLATION_REQUIRED.",
    },
    "JUR-TN": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministère de l'Éducation (Tunisia)",
        "notes": "National programmes scolaires; Arabic/French — TRANSLATION_REQUIRED.",
    },
    "JUR-UG": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Sports / NCDC (Uganda)",
        "notes": "Lower Secondary Curriculum / primary instruments via NCDC; deeper early-years pins pending.",
    },
    "JUR-ZM": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Zambia)",
        "notes": "Zambia Education Curriculum Framework identified; deeper subject PDF pins pending.",
    },
    "JUR-ZW": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Primary and Secondary Education (Zimbabwe)",
        "notes": "Competence-based curriculum instruments identified; deeper PDF edition pins pending.",
    },
    # deepen already-IDENTIFIED Africa
    "JUR-EG": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Technical Education (Egypt)",
        "notes": "National curriculum / Education 2.0 reform materials identified; Arabic primary — TRANSLATION_REQUIRED.",
    },
    "JUR-GH": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ghana Education Service / NaCCA",
        "framework_ids": ["FW-GH-SBC"],
        "notes": "Standards-Based Curriculum (NaCCA) identified via official channels; deep domain maps pending.",
    },
    "JUR-KE": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "Ministry of Education (Kenya) / KICD",
        "framework_ids": ["FW-KE-BECF-2019"],
        "notes": "Basic Education Curriculum Framework (CBC) verified via KICD portal (kicd.ac.ke).",
    },
    "JUR-NG": {
        "research_status": "IDENTIFIED",
        "education_authority": "Federal Ministry of Education / NERDC (Nigeria)",
        "notes": "National Curriculum / NERDC instruments identified at high level; deeper subject pins pending.",
    },
    "JUR-ZA": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "Department of Basic Education (South Africa)",
        "framework_ids": ["FW-ZA-CAPS", "FW-ZA-CODING-ROBOTICS"],
        "notes": (
            "CAPS Foundation/Intermediate portals verified on education.gov.za; "
            "Coding & Robotics CAPS Grades R–9 (Umalusi-endorsed path; Foundation Phase rollout programme) pinned via DBE draft/portal docs."
        ),
    },
    # --- Middle East ---
    "JUR-BH": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Bahrain)",
        "framework_ids": ["FW-BH-NCF"],
        "notes": "National Curriculum Framework (+ ECE NCF) on moe.gov.bh; Arabic primary — TRANSLATION_REQUIRED.",
    },
    "JUR-IR": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Iran)",
        "notes": "National curriculum / formal school programmes; Persian primary — TRANSLATION_REQUIRED.",
    },
    "JUR-IQ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Iraq)",
        "notes": "National curriculum instruments; Arabic primary — TRANSLATION_REQUIRED; portal access variable.",
    },
    "JUR-IL": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Israel)",
        "notes": "National curriculum / pedagogical portal instruments identified; Hebrew/Arabic depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-JO": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Jordan)",
        "notes": "General Curriculum Framework (الإطار العام للمناهج الأردنية) identified; Arabic primary — TRANSLATION_REQUIRED.",
    },
    "JUR-KW": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Kuwait)",
        "notes": "Kuwait National Curriculum Framework (competence-/standards-based) identified; Arabic primary — TRANSLATION_REQUIRED.",
    },
    "JUR-LB": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Higher Education (Lebanon) / CERD",
        "notes": "National curriculum / CERD instruments; Arabic/French — TRANSLATION_REQUIRED.",
    },
    "JUR-OM": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Oman)",
        "notes": "National study plan / curriculum instruments on home.moe.gov.om; Arabic primary — TRANSLATION_REQUIRED.",
    },
    "JUR-PS": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Higher Education (State of Palestine)",
        "notes": "National curriculum instruments; Arabic primary — TRANSLATION_REQUIRED; access conditions vary.",
    },
    "JUR-QA": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Higher Education (Qatar)",
        "notes": "Qatar National Curriculum Framework identified; Arabic primary — TRANSLATION_REQUIRED.",
    },
    "JUR-SY": {
        "research_status": "ACCESS_BLOCKED",
        "education_authority": "Ministry of Education (Syrian Arab Republic)",
        "notes": "Conflict-era access: stable official curriculum corpus not reliably open-access for verification.",
    },
    "JUR-YE": {
        "research_status": "ACCESS_BLOCKED",
        "education_authority": "Ministry of Education (Yemen)",
        "notes": "Conflict-era access: stable official curriculum corpus not reliably open-access for verification.",
    },
    "JUR-SA": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Saudi Arabia)",
        "notes": "National curriculum modernization / Vision 2030 education instruments identified; Arabic depth TRANSLATION_REQUIRED for clause work.",
    },
    "JUR-AE": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (UAE) + emirate authorities (e.g. ADEK, KHDA)",
        "notes": "Federal MoE framework + emirate variation (Abu Dhabi/Dubai); deeper emirate census still open.",
    },
    # --- Asia-Pacific ---
    "JUR-AF": {
        "research_status": "ACCESS_BLOCKED",
        "education_authority": "Ministry of Education (Afghanistan)",
        "notes": "Post-2021 access: stable official early-years/primary curriculum corpus not reliably open-access.",
    },
    "JUR-BD": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education / NCTB (Bangladesh)",
        "notes": "National Curriculum Framework / NCTB instruments identified; Bangla depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-BT": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Skills Development (Bhutan)",
        "notes": "National school curriculum / early learning instruments identified via MoESD.",
    },
    "JUR-BN": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Brunei Darussalam)",
        "notes": "National curriculum / SPN21 instruments identified; Malay depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-KH": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education, Youth and Sport (Cambodia)",
        "notes": "National curriculum instruments; Khmer primary — TRANSLATION_REQUIRED.",
    },
    "JUR-FJ": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Fiji)",
        "notes": "National curriculum framework / syllabus instruments identified.",
    },
    "JUR-ID": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education, Culture, Research and Technology / Kemendikbudristek (Indonesia)",
        "framework_ids": ["FW-ID-KURIKULUM-MERDEKA"],
        "notes": "Kurikulum Merdeka mandated as national curriculum (MoECRT Reg. 12/2024); Indonesian primary — TRANSLATION_REQUIRED for depth.",
    },
    "JUR-KZ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Kazakhstan)",
        "notes": "State compulsory education standards; Kazakh/Russian — TRANSLATION_REQUIRED.",
    },
    "JUR-KI": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Kiribati)",
        "notes": "National curriculum instruments identified at high level; limited public PDF depth.",
    },
    "JUR-KG": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Science (Kyrgyzstan)",
        "notes": "State education standards; Kyrgyz/Russian — TRANSLATION_REQUIRED.",
    },
    "JUR-LA": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Sports (Lao PDR)",
        "notes": "National curriculum; Lao primary — TRANSLATION_REQUIRED.",
    },
    "JUR-MY": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Malaysia)",
        "framework_ids": ["FW-MY-KSSR"],
        "notes": "KSSR (Kurikulum Standard Sekolah Rendah) + preschool standards identified via MoE; Malay depth TRANSLATION_REQUIRED for clause work.",
    },
    "JUR-MV": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Maldives)",
        "notes": "National Curriculum Framework identified; Dhivehi depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-MH": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education, Sports and Training (Marshall Islands)",
        "notes": "National curriculum instruments identified at high level; limited public PDF depth.",
    },
    "JUR-FM": {
        "research_status": "IDENTIFIED",
        "education_authority": "National Department of Education (Federated States of Micronesia)",
        "notes": "National / state education standards identified at high level; limited public PDF depth.",
    },
    "JUR-MN": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Science (Mongolia)",
        "notes": "National core curriculum; Mongolian primary — TRANSLATION_REQUIRED.",
    },
    "JUR-MM": {
        "research_status": "ACCESS_BLOCKED",
        "education_authority": "Ministry of Education (Myanmar)",
        "notes": "Conflict/transition-era access: stable official curriculum corpus not reliably open-access for verification.",
    },
    "JUR-NR": {
        "research_status": "IDENTIFIED",
        "education_authority": "Department of Education and Training (Nauru)",
        "notes": "National curriculum instruments identified at high level; limited public PDF depth.",
    },
    "JUR-NP": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education, Science and Technology / CDC (Nepal)",
        "notes": "National Curriculum Framework / CDC instruments identified; Nepali depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-KP": {
        "research_status": "ACCESS_BLOCKED",
        "education_authority": "Education Commission / MoE (DPRK)",
        "notes": "Official curriculum corpus not publicly accessible for independent verification.",
    },
    "JUR-PK": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Federal Education and Professional Training / NCC (Pakistan)",
        "notes": "Single National Curriculum / National Curriculum of Pakistan instruments identified; Urdu depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-PW": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education (Palau)",
        "notes": "National curriculum instruments identified at high level; limited public PDF depth.",
    },
    "JUR-PG": {
        "research_status": "IDENTIFIED",
        "education_authority": "Department of Education (Papua New Guinea)",
        "notes": "National curriculum / standards instruments identified; deeper PDF pins pending.",
    },
    "JUR-PH": {
        "research_status": "IDENTIFIED",
        "education_authority": "Department of Education (DepEd), Philippines",
        "framework_ids": ["FW-PH-MATATAG"],
        "notes": "MATATAG Curriculum policy guidelines (DepEd Order No. 10, s. 2024) identified; phased K/1/4/7 start SY 2024–25.",
    },
    "JUR-WS": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Culture (Samoa)",
        "notes": "National curriculum instruments identified; Samoan depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-SB": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Human Resources Development (Solomon Islands)",
        "notes": "National curriculum instruments identified at high level.",
    },
    "JUR-LK": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education / NIE (Sri Lanka)",
        "notes": "National curriculum / NIE instruments identified; Sinhala/Tamil depth may need TRANSLATION_REQUIRED.",
    },
    "JUR-TJ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Science (Tajikistan)",
        "notes": "State education standards; Tajik/Russian — TRANSLATION_REQUIRED.",
    },
    "JUR-TH": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education / OBEC (Thailand)",
        "notes": "Basic Education Core Curriculum B.E. 2551 (+ updates); Thai primary — TRANSLATION_REQUIRED.",
    },
    "JUR-TL": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministério da Educação, Juventude e Desporto (Timor-Leste)",
        "notes": "National curriculum; Portuguese/Tetum — TRANSLATION_REQUIRED.",
    },
    "JUR-TO": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Training (Tonga)",
        "notes": "National curriculum instruments identified at high level.",
    },
    "JUR-TM": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Turkmenistan)",
        "notes": "State education programmes; Turkmen/Russian — TRANSLATION_REQUIRED; limited English portal depth.",
    },
    "JUR-TV": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Sports (Tuvalu)",
        "notes": "National curriculum instruments identified at high level; limited public PDF depth.",
    },
    "JUR-UZ": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Preschool and School Education (Uzbekistan)",
        "notes": "National curriculum / preschool standards; Uzbek/Russian — TRANSLATION_REQUIRED.",
    },
    "JUR-VU": {
        "research_status": "IDENTIFIED",
        "education_authority": "Ministry of Education and Training (Vanuatu)",
        "notes": "National curriculum instruments identified; French/Bislama streams may need TRANSLATION_REQUIRED.",
    },
    "JUR-VN": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education and Training (Viet Nam)",
        "notes": "2018 General Education Curriculum; Vietnamese primary — TRANSLATION_REQUIRED.",
    },
    # deepen APAC baselines + China/Korea
    "JUR-AU": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "Australian Government Department of Education / ACECQA / ACARA",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": (
            "EYLF V2.0 (2022) PDF pinned via ACECQA; Australian Curriculum v9 portal verified. "
            "States/territories adopt or adapt v9 on their own timelines (NESA NSW; Victorian Curriculum F–10 v2; "
            "QCAA/ACT/SA/TAS/NT largely teach AC v9; WA Curriculum closely based)."
        ),
    },
    "JUR-NZ": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "Ministry of Education (New Zealand)",
        "framework_ids": ["FW-NZ-TE-WHARIKI", "FW-NZ-NZC"],
        "notes": (
            "Te Whāriki (2017) on Tāhūrangi; NZC 2007 still required framework while Te Mātaiaho draft "
            "(Oct 2025, consultation to Apr 2026; Gazette mid-2026 planned) is familiarisation-only."
        ),
    },
    "JUR-IN": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "NCERT / Ministry of Education (India)",
        "framework_ids": ["FW-IN-NCF-FOUNDATIONAL", "FW-IN-NCF-SE-2023"],
        "notes": "NCF-FS 2022 + NCF-SE 2023 (broader national framework ages 3–18) verified via NCERT/MoE PDFs.",
    },
    "JUR-SG": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "Ministry of Education (Singapore)",
        "framework_ids": ["FW-SG-NEL-2022", "FW-SG-NDLP-DLTS"],
        "notes": "NEL Framework 2022 + National Digital Literacy Programme / EdTech Masterplan 2030 DLTS verified on moe.gov.sg.",
    },
    "JUR-JP": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "MEXT (Japan)",
        "framework_ids": ["FW-JP-MEXT-COS"],
        "notes": (
            "Heisei 29 (2017) kindergarten guidelines + elementary Courses of Study pinned on mext.go.jp "
            "(平成29・30・31年改訂); Japanese primary texts — deep clause maps TRANSLATION_REQUIRED."
        ),
    },
    "JUR-CN": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (China)",
        "notes": "National curriculum standards / kindergarten guidelines; Chinese primary — TRANSLATION_REQUIRED.",
    },
    "JUR-KR": {
        "research_status": "TRANSLATION_REQUIRED",
        "education_authority": "Ministry of Education (Republic of Korea)",
        "notes": "Nuri curriculum / national curriculum revisions; Korean primary — TRANSLATION_REQUIRED.",
    },
    # Australia states/territories — state implications
    "JUR-AU-NSW": {
        "research_status": "IDENTIFIED",
        "education_authority": "NSW Education Standards Authority (NESA)",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "NESA syllabuses adopt/adapt Australian Curriculum v9 into NSW Stages; EYLF V2.0 under NQF for ECEC.",
    },
    "JUR-AU-VIC": {
        "research_status": "IDENTIFIED",
        "education_authority": "Victorian Curriculum and Assessment Authority (VCAA)",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "Victorian Curriculum F–10 Version 2.0 informed by AC v9 (restructured levels/codes); EYLF V2.0 under NQF.",
    },
    "JUR-AU-QLD": {
        "research_status": "IDENTIFIED",
        "education_authority": "Queensland Curriculum and Assessment Authority (QCAA) / DoE",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "Teaches Australian Curriculum v9 directly; QCAA phased implementation with full learning-area expectation by end-2027.",
    },
    "JUR-AU-WA": {
        "research_status": "IDENTIFIED",
        "education_authority": "School Curriculum and Standards Authority (SCSA), Western Australia",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "Western Australian Curriculum closely based on / adapting AC v9; phased subject rollout toward mid-decade.",
    },
    "JUR-AU-SA": {
        "research_status": "IDENTIFIED",
        "education_authority": "Department for Education (South Australia)",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "Teaches Australian Curriculum v9 essentially as published; EYLF V2.0 under NQF.",
    },
    "JUR-AU-TAS": {
        "research_status": "IDENTIFIED",
        "education_authority": "Department for Education, Children and Young People (Tasmania)",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "Teaches Australian Curriculum v9 essentially as published; EYLF V2.0 under NQF.",
    },
    "JUR-AU-ACT": {
        "research_status": "IDENTIFIED",
        "education_authority": "Education Directorate (ACT)",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "Teaches Australian Curriculum v9 essentially as published; EYLF V2.0 under NQF.",
    },
    "JUR-AU-NT": {
        "research_status": "IDENTIFIED",
        "education_authority": "Department of Education and Training (Northern Territory)",
        "framework_ids": ["FW-AU-EYLF-V2", "FW-AU-AC-V9"],
        "notes": "Staged AC v9 rollout (English/Maths/HPE by 2025; Technologies etc. by 2026 per NT guidance); EYLF V2.0 under NQF.",
    },
    "JUR-GLOBAL-UNESCO": {
        "research_status": "OFFICIAL_VERIFIED",
        "education_authority": "UNESCO",
        "framework_ids": [
            "FW-UNESCO-AI-STUDENTS-2024",
            "FW-UNESCO-AI-TEACHERS-2024",
            "FW-UNESCO-ICT-CFT",
            "FW-UNESCO-SDG4-ED2030",
            "FW-UNESCO-MIL-2021",
        ],
        "notes": "Global reference frameworks under SDG 4 (Education 2030) — not a national curriculum. Includes AI students/teachers, MIL 2nd ed., ICT-CFT.",
    },
}

# ---------------------------------------------------------------------------
# Framework upserts / patches
# ---------------------------------------------------------------------------

NEW_FRAMEWORKS: list[dict] = [
    {
        "framework_id": "FW-UNESCO-SDG4-ED2030",
        "title": "SDG 4 — Education 2030 (global education goal / cooperation framework)",
        "authority": "UNESCO (custodian) / UN Member States",
        "framework_class": "TRANSVERSAL",
        "version": "Education 2030 Agenda (ongoing; HLSC stewardship)",
        "effective_from": "2015",
        "url": "https://www.unesco.org/sdg4education2030/en",
        "license_note": "UNESCO / UN copyright; summarize only",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "jurisdiction_ids": ["JUR-GLOBAL-UNESCO"],
        "language": ["en"],
        "age_relevance": ["K2", "K3", "K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": [
            "inclusive equitable quality education",
            "lifelong learning",
            "global education cooperation",
        ],
        "gaps": [],
        "mandatory_baseline": True,
    },
    {
        "framework_id": "FW-UNESCO-MIL-2021",
        "title": "Media and Information Literate Citizens: Think Critically, Click Wisely (MIL Curriculum 2nd ed.)",
        "authority": "UNESCO",
        "framework_class": "DIGITAL_COMPETENCE",
        "version": "Second Edition (2021); ISBN 978-92-3-100448-3",
        "effective_from": "2021",
        "url": "https://www.unesco.org/mil4teachers/en/curriculum",
        "license_note": "UNESCO copyright; summarize only — do not paste wholesale",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "jurisdiction_ids": ["JUR-GLOBAL-UNESCO"],
        "language": ["en"],
        "age_relevance": ["B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": [
            "media and information literacy",
            "disinformation resilience",
            "digital citizenship",
            "AI-aware MIL",
        ],
        "gaps": [],
        "mandatory_baseline": True,
    },
    {
        "framework_id": "FW-IN-NCF-SE-2023",
        "title": "National Curriculum Framework for School Education (NCF-SE)",
        "authority": "NCERT / Ministry of Education (India)",
        "framework_class": "PRIMARY",
        "version": "NCF-SE 2023 (August 2023 PDF; NCERT print Oct 2024 Kartika 1946)",
        "effective_from": "2023",
        "url": "https://ncert.nic.in/pdf/NCFSE-2023-August_2023.pdf",
        "license_note": "NCERT / Government of India copyright; summarize only",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "jurisdiction_ids": ["JUR-IN"],
        "language": ["en", "hi"],
        "age_relevance": ["K2", "K3", "K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": [
            "5+3+3+4 structure",
            "integrates NCF-FS",
            "holistic development",
            "subject learning standards",
        ],
        "gaps": [],
        "mandatory_baseline": True,
    },
    {
        "framework_id": "FW-SG-NDLP-DLTS",
        "title": "National Digital Literacy Programme / Digital Literacy and Technological Skills (EdTech Masterplan 2030)",
        "authority": "Ministry of Education (Singapore)",
        "framework_class": "DIGITAL_COMPETENCE",
        "version": "NDLP (2020 launch); EdTech Masterplan 2030 9 digital competencies (portal updated 2025-12-05)",
        "effective_from": "2020",
        "url": "https://www.moe.gov.sg/education-in-sg/educational-technology-journey/edtech-masterplan/digital-literacy-and-technological-skills",
        "license_note": "MOE Singapore copyright; summarize only",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "jurisdiction_ids": ["JUR-SG"],
        "language": ["en"],
        "age_relevance": ["K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": [
            "Find-Think-Apply-Create",
            "computational thinking",
            "coding and programming",
            "digital safety",
            "AI literacy (technological skills)",
        ],
        "gaps": [],
        "mandatory_baseline": True,
    },
    {
        "framework_id": "FW-KE-BECF-2019",
        "title": "Basic Education Curriculum Framework (Kenya CBC)",
        "authority": "Kenya Institute of Curriculum Development (KICD)",
        "framework_class": "PRIMARY",
        "version": "BECF 2019 (CBC materials live on kicd.ac.ke)",
        "effective_from": "2019",
        "url": "https://kicd.ac.ke/cbc-materials/",
        "license_note": "KICD copyright; summarize only",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "jurisdiction_ids": ["JUR-KE"],
        "language": ["en"],
        "age_relevance": ["K3", "K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["core competencies", "learning areas", "values-based education"],
        "gaps": [],
        "mandatory_baseline": False,
    },
    {
        "framework_id": "FW-ET-CURRICULUM-FRAMEWORK",
        "title": "Curriculum Framework for Ethiopian Education (KG – Grade 12)",
        "authority": "Ministry of Education (Ethiopia)",
        "framework_class": "PRIMARY",
        "version": "May 2009 framework (portal-hosted); confirm successor editions before clause maps",
        "effective_from": "2009",
        "url": "https://moe.gov.et/storage/Books/Curriculum%20Framework%20for%20Ethiopian%20Education%20(KG%20%E2%80%93%20Grade%2012).pdf",
        "license_note": "MoE Ethiopia copyright; summarize only",
        "retrieved_on": REVIEWED,
        "verification": "IDENTIFIED",
        "jurisdiction_ids": ["JUR-ET"],
        "language": ["en"],
        "age_relevance": ["K3", "K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["competency-based approach", "active learning", "KG–12 structure"],
        "gaps": ["SOURCE_VERSION_UNCLEAR", "confirm post-2009 successor frameworks"],
        "mandatory_baseline": False,
    },
    {
        "framework_id": "FW-RW-CBC",
        "title": "Competence-Based Curriculum Framework (Rwanda)",
        "authority": "Ministry of Education / Rwanda Education Board (REB)",
        "framework_class": "PRIMARY",
        "version": "CBC Framework (competence-based; confirm exact REB PDF edition)",
        "effective_from": None,
        "url": "https://www.reb.rw/",
        "license_note": "REB / MoE copyright",
        "retrieved_on": REVIEWED,
        "verification": "IDENTIFIED",
        "jurisdiction_ids": ["JUR-RW"],
        "language": ["en"],
        "age_relevance": ["K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["competences", "subject syllabi", "assessment"],
        "gaps": ["SOURCE_VERSION_UNCLEAR", "NOT_YET_MAPPED"],
        "mandatory_baseline": False,
    },
    {
        "framework_id": "FW-GH-SBC",
        "title": "Standards-Based Curriculum (Ghana)",
        "authority": "National Council for Curriculum and Assessment (NaCCA) / GES",
        "framework_class": "PRIMARY",
        "version": "Standards-Based Curriculum (confirm current NaCCA PDF edition)",
        "effective_from": None,
        "url": "https://nacca.gov.gh/",
        "license_note": "NaCCA copyright",
        "retrieved_on": REVIEWED,
        "verification": "IDENTIFIED",
        "jurisdiction_ids": ["JUR-GH"],
        "language": ["en"],
        "age_relevance": ["K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["standards-based learning", "core competencies"],
        "gaps": ["SOURCE_VERSION_UNCLEAR", "NOT_YET_MAPPED"],
        "mandatory_baseline": False,
    },
    {
        "framework_id": "FW-BH-NCF",
        "title": "National Curriculum Framework (Bahrain) + Early Childhood Education NCF",
        "authority": "Ministry of Education (Bahrain)",
        "framework_class": "PRIMARY",
        "version": "NCF (+ ECE NCF listed on moe.gov.bh; Arabic primary)",
        "effective_from": None,
        "url": "https://moe.gov.bh/en/the-national-curriculum-framework",
        "license_note": "MoE Bahrain copyright",
        "retrieved_on": REVIEWED,
        "verification": "IDENTIFIED",
        "jurisdiction_ids": ["JUR-BH"],
        "language": ["ar", "en"],
        "age_relevance": ["K2", "K3", "K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["national curriculum framework", "early childhood education"],
        "gaps": ["TRANSLATION_REQUIRED", "SOURCE_VERSION_UNCLEAR"],
        "mandatory_baseline": False,
    },
    {
        "framework_id": "FW-ID-KURIKULUM-MERDEKA",
        "title": "Kurikulum Merdeka (Emancipated Curriculum)",
        "authority": "Kemendikbudristek (Indonesia)",
        "framework_class": "PRIMARY",
        "version": "National mandate via MoECRT Regulation No. 12/2024 (from July 2024)",
        "effective_from": "2024",
        "url": "https://kurikulum.kemdikbud.go.id/",
        "license_note": "Kemendikbudristek copyright; Indonesian primary",
        "retrieved_on": REVIEWED,
        "verification": "IDENTIFIED",
        "jurisdiction_ids": ["JUR-ID"],
        "language": ["id"],
        "age_relevance": ["K3", "K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["differentiated learning", "Pancasila learner profile (P5)", "flexibility"],
        "gaps": ["TRANSLATION_REQUIRED", "NOT_YET_MAPPED"],
        "mandatory_baseline": False,
    },
    {
        "framework_id": "FW-MY-KSSR",
        "title": "Kurikulum Standard Sekolah Rendah (KSSR) + Kurikulum Standard Prasekolah Kebangsaan",
        "authority": "Ministry of Education (Malaysia)",
        "framework_class": "PRIMARY",
        "version": "KSSR / national preschool standards (confirm current DSPK PDF edition)",
        "effective_from": None,
        "url": "https://www.moe.gov.my/",
        "license_note": "MoE Malaysia copyright; Malay primary",
        "retrieved_on": REVIEWED,
        "verification": "IDENTIFIED",
        "jurisdiction_ids": ["JUR-MY"],
        "language": ["ms", "en"],
        "age_relevance": ["K3", "K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["standard-based primary", "preschool standards", "STEM integration"],
        "gaps": ["TRANSLATION_REQUIRED", "SOURCE_VERSION_UNCLEAR", "NOT_YET_MAPPED"],
        "mandatory_baseline": False,
    },
    {
        "framework_id": "FW-PH-MATATAG",
        "title": "MATATAG Curriculum (Philippines)",
        "authority": "Department of Education (DepEd)",
        "framework_class": "PRIMARY",
        "version": "DepEd Order No. 10, s. 2024 (phased K/1/4/7 from SY 2024–25)",
        "effective_from": "2024",
        "url": "https://www.deped.gov.ph/wp-content/uploads/DO_s2024_010.pdf",
        "license_note": "DepEd copyright; summarize only",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "jurisdiction_ids": ["JUR-PH"],
        "language": ["en"],
        "age_relevance": ["K4", "K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"],
        "summary_domains": ["MATATAG learning areas", "instructional planning standards"],
        "gaps": [],
        "mandatory_baseline": False,
    },
]

FW_PATCHES: dict[str, dict] = {
    "FW-AU-EYLF-V2": {
        "version": "V2.0 (2022); AGDE for Ministerial Council; ACECQA approved under NQF",
        "url": "https://www.acecqa.gov.au/sites/default/files/2023-01/EYLF-2022-V2.0.pdf",
        "effective_from": "2023",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": [],
        "summary_domains": [
            "Belonging Being Becoming",
            "principles",
            "practices",
            "five learning outcomes",
            "transition to school",
        ],
    },
    "FW-AU-AC-V9": {
        "version": "Version 9.0 (endorsed 2022; state/territory implementation timelines vary)",
        "url": "https://v9.australiancurriculum.edu.au/",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": [],
        "summary_domains": [
            "Digital Technologies (incl. privacy/security)",
            "Science",
            "general capabilities",
            "F–10 learning areas",
        ],
        "notes": (
            "States/territories determine take-up: NSW NESA adapt; VIC Victorian Curriculum F–10 v2; "
            "QLD/SA/TAS/ACT/NT largely teach AC v9; WA Curriculum closely based."
        ),
    },
    "FW-NZ-TE-WHARIKI": {
        "version": "2017 (He whāriki mātauranga mō ngā mokopuna o Aotearoa); ISBN 978-0-478-16927-0 (online)",
        "url": "https://tewhariki.tahurangi.education.govt.nz/early-childhood-curriculum-home",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": [],
        "summary_domains": [
            "principles",
            "strands",
            "goals",
            "learning outcomes",
            "bicultural curriculum",
        ],
    },
    "FW-NZ-NZC": {
        "title": "The New Zealand Curriculum (NZC 2007 required) / Te Mātaiaho draft refresh",
        "version": (
            "NZC 2007 still the required framework; Te Mātaiaho draft Oct 2025 "
            "(consultation to 2026-04-24; Gazette mid-2026 planned)"
        ),
        "url": "https://newzealandcurriculum.tahurangi.education.govt.nz/",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": [
            "Te Mātaiaho still draft at retrieval — do not treat draft learning-area text as gazetted",
        ],
        "summary_domains": [
            "key competencies",
            "learning areas including technology / hāngarau",
            "Te Mātaiaho knowledge-rich sequencing (draft)",
        ],
    },
    "FW-IN-NCF-FOUNDATIONAL": {
        "version": "NCF-FS 2022 (20 October 2022 PDF)",
        "url": "https://ncert.nic.in/pdf/NCF_for_Foundational_Stage_20_October_2022.pdf",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": [],
        "summary_domains": [
            "foundational literacy and numeracy",
            "play-based learning",
            "ages 3–8 Foundational Stage",
            "holistic development",
        ],
    },
    "FW-SG-NEL-2022": {
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": [],
    },
    "FW-JP-MEXT-COS": {
        "title": "Courses of Study — Kindergarten guidelines + Elementary (MEXT Heisei 29 revision)",
        "version": "平成29年改訂 (2017 notification); elementary fully in force from 2020 (令和2)",
        "url": "https://www.mext.go.jp/a_menu/shotou/new-cs/1384661.htm",
        "effective_from": "2018-04-01",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": ["TRANSLATION_REQUIRED"],
        "summary_domains": [
            "幼稚園教育要領 five areas",
            "小学校学習指導要領 subjects + ICT",
            "three pillars of qualities/abilities",
            "proactive interactive deep learning",
        ],
        "language": ["ja", "en"],
    },
    "FW-ZA-CAPS": {
        "version": "National Curriculum Statement Grades R–12 / CAPS subject statements (Foundation + Intermediate portals)",
        "url": "https://www.education.gov.za/Curriculum/CurriculumAssessmentPolicyStatements(CAPS).aspx",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": ["pin individual subject PDF editions when mapping clause-level"],
        "summary_domains": [
            "Foundation Phase",
            "Intermediate Phase",
            "subject CAPS policies",
            "assessment policy",
        ],
    },
    "FW-ZA-CODING-ROBOTICS": {
        "title": "CAPS Coding and Robotics (Grades R–9)",
        "version": (
            "CAPS Coding & Robotics Grades R–9 (Umalusi-approved path Feb 2024 per DBE reporting; "
            "Foundation Phase rollout programme; draft PDFs on education.gov.za)"
        ),
        "url": "https://www.education.gov.za/DraftCapsCodingRobotics.aspx",
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "gaps": [
            "prefer final gazetted phase PDFs over draft call-for-comments files when available",
        ],
        "summary_domains": [
            "Pattern Recognition",
            "Algorithms and Coding",
            "Robotics Skills",
            "Internet and e-communication",
            "Application Skills",
            "computational thinking",
        ],
    },
    "FW-OECD-LEARNING-COMPASS-2030": {
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
        "url": "https://www.oecd.org/en/data/tools/oecd-learning-compass-2030.html",
    },
    "FW-UNESCO-AI-STUDENTS-2024": {
        "retrieved_on": REVIEWED,
        "verification": "OFFICIAL_VERIFIED",
    },
}

NEW_MAPPINGS: list[dict] = [
    {
        "mapping_id": "MAP-AU-AC-DT-ADJ",
        "relationship": "CROSSWALKED_AGAINST",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-AU-AC-V9",
        "from_node": "Digital Technologies F–2 (sequences, data, digital systems grain)",
        "to_kids_target_id": "KE-TARGET-ALGO-FOUNDATIONS",
        "kids_bands": ["K5", "K6", "K7"],
        "notes": DISCLAIMER + " State delivery via AC v9 or state adaptions (NESA/VCAA/SCSA).",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-NZC-TECH-ADJ",
        "relationship": "MAPPED_TO",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-NZ-NZC",
        "from_node": "Technology / hāngarau learning area (NZC 2007; Te Mātaiaho draft sequencing TBD)",
        "to_kids_target_id": "KE-TARGET-ALGO-FOUNDATIONS",
        "kids_bands": ["K6", "K7", "B5", "B6"],
        "notes": DISCLAIMER + " Do not treat Te Mātaiaho draft as gazetted.",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-NCFSE-SCI-ADJ",
        "relationship": "MAPPED_TO",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-IN-NCF-SE-2023",
        "from_node": "Preparatory/Middle stage science & inquiry practices (domain-family grain)",
        "to_kids_target_id": "KE-TARGET-SCIENCE-PRACTICES",
        "kids_bands": ["K6", "K7", "B5", "B6", "B7"],
        "notes": DISCLAIMER,
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-SG-DLTS-ADJ",
        "relationship": "CROSSWALKED_AGAINST",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-SG-NDLP-DLTS",
        "from_node": "Computational thinking / coding & programming competencies (primary grain)",
        "to_kids_target_id": "KE-TARGET-ALGO-FOUNDATIONS",
        "kids_bands": ["K6", "K7", "B5", "B6", "B7"],
        "notes": DISCLAIMER,
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-SG-DLTS-CITIZEN-ADJ",
        "relationship": "MAPPED_TO",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-SG-NDLP-DLTS",
        "from_node": "Digital safety, responsibility, information management",
        "to_kids_target_id": "KE-TARGET-DIGITAL-CITIZENSHIP",
        "kids_bands": ["K5", "K6", "K7", "B5", "B6", "B7", "B8"],
        "notes": DISCLAIMER,
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-JP-COS-PLAY-ADJ",
        "relationship": "MAPPED_TO",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-JP-MEXT-COS",
        "from_node": "Kindergarten five areas / play-centred environment (domain-family; JP primary text)",
        "to_kids_target_id": "KE-TARGET-PLAY-INQUIRY",
        "kids_bands": ["K3", "K4", "K5"],
        "notes": DISCLAIMER + " TRANSLATION_REQUIRED before fidelity upgrade.",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-JP-COS-ICT-ADJ",
        "relationship": "MAPPED_TO",
        "fidelity": "PROPOSED",
        "from_framework_id": "FW-JP-MEXT-COS",
        "from_node": "Elementary ICT / programming education elements (Heisei 29)",
        "to_kids_target_id": "KE-TARGET-ALGO-FOUNDATIONS",
        "kids_bands": ["K6", "K7", "B5", "B6"],
        "notes": DISCLAIMER + " TRANSLATION_REQUIRED; proposed editorial grain only.",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-CAPS-SCI-ADJ",
        "relationship": "CROSSWALKED_AGAINST",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-ZA-CAPS",
        "from_node": "Foundation/Intermediate Natural Sciences and Technology (domain-family)",
        "to_kids_target_id": "KE-TARGET-SCIENCE-PRACTICES",
        "kids_bands": ["K5", "K6", "K7", "B5", "B6"],
        "notes": DISCLAIMER + " Subject PDF editions still pin-per-subject for clause work.",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-ZA-CODING-ADJ",
        "relationship": "CROSSWALKED_AGAINST",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-ZA-CODING-ROBOTICS",
        "from_node": "Foundation Phase Algorithms and Coding / Pattern Recognition strands",
        "to_kids_target_id": "KE-TARGET-ALGO-FOUNDATIONS",
        "kids_bands": ["K5", "K6", "K7", "B5", "B6"],
        "notes": DISCLAIMER + " Prefer final gazetted PDFs when available over draft call-for-comments.",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-UNESCO-MIL-CITIZEN-ADJ",
        "relationship": "MAPPED_TO",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-UNESCO-MIL-2021",
        "from_node": "MIL competencies for critical engagement with media/information",
        "to_kids_target_id": "KE-TARGET-DIGITAL-CITIZENSHIP",
        "kids_bands": ["B5", "B6", "B7", "B8", "B9", "B10"],
        "notes": DISCLAIMER + " Educator/learner curriculum — age-band downshift is editorial.",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-UNESCO-SDG4-INFORM",
        "relationship": "INFORMED_BY",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-UNESCO-SDG4-ED2030",
        "from_node": "SDG 4 quality education / lifelong learning aspiration",
        "to_kids_target_id": "KE-TARGET-PLAY-INQUIRY",
        "kids_bands": ["K2", "K3", "K4", "K5"],
        "notes": DISCLAIMER + " Transnational aspiration — not a curriculum standard.",
        "reviewed_on": REVIEWED,
    },
    {
        "mapping_id": "MAP-OECD-COMPASS-INFORM",
        "relationship": "INFORMED_BY",
        "fidelity": "ADJACENT",
        "from_framework_id": "FW-OECD-LEARNING-COMPASS-2030",
        "from_node": "Transformative competencies / learner agency (high-level)",
        "to_kids_target_id": "KE-TARGET-SYSTEMS-STABILITY",
        "kids_bands": ["B5", "B6", "B7", "B8"],
        "notes": DISCLAIMER + " Evolving concept-note set; not a fixed edition PDF.",
        "reviewed_on": REVIEWED,
    },
]


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be mapping")
    return data


def dump_yaml(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True,
            width=100,
            default_flow_style=False,
        )


def patch_jurisdictions(jur: dict) -> tuple[dict, dict]:
    before: dict[str, Counter] = {}
    for region in ("africa", "middle_east", "asia_pacific"):
        rows = [j for j in jur["jurisdictions"] if j.get("region") == region]
        before[region] = Counter(j.get("research_status") for j in rows)

    for row in jur["jurisdictions"]:
        jid = row["jurisdiction_id"]
        if jid not in JUR_RESEARCH:
            continue
        upd = JUR_RESEARCH[jid]
        row["research_status"] = upd["research_status"]
        if "education_authority" in upd:
            row["education_authority"] = upd["education_authority"]
        if "framework_ids" in upd:
            row["framework_ids"] = list(upd["framework_ids"])
        row["notes"] = upd["notes"]
        row["last_reviewed_on"] = REVIEWED

    # recompute counts
    statuses = Counter(j.get("research_status") for j in jur["jurisdictions"])
    jur["counts"]["by_status"] = {
        "OFFICIAL_VERIFIED": statuses.get("OFFICIAL_VERIFIED", 0),
        "IDENTIFIED": statuses.get("IDENTIFIED", 0),
        "TRANSLATION_REQUIRED": statuses.get("TRANSLATION_REQUIRED", 0),
        "ACCESS_BLOCKED": statuses.get("ACCESS_BLOCKED", 0),
        "NOT_YET_RESEARCHED": statuses.get("NOT_YET_RESEARCHED", 0),
        "SOURCE_VERSION_UNCLEAR": statuses.get("SOURCE_VERSION_UNCLEAR", 0),
    }
    # drop zero optional keys for clarity? keep schema stable — include zeros only if present before
    jur["counts"]["by_status"] = {k: v for k, v in jur["counts"]["by_status"].items() if v or k in ("OFFICIAL_VERIFIED", "IDENTIFIED", "NOT_YET_RESEARCHED", "TRANSLATION_REQUIRED", "ACCESS_BLOCKED")}
    jur["generated_on"] = REVIEWED

    after: dict[str, Counter] = {}
    for region in ("africa", "middle_east", "asia_pacific"):
        rows = [j for j in jur["jurisdictions"] if j.get("region") == region]
        after[region] = Counter(j.get("research_status") for j in rows)
    return before, after


def patch_sources(src: dict) -> None:
    by_id = {f["framework_id"]: f for f in src["frameworks"]}
    for fid, patch in FW_PATCHES.items():
        if fid not in by_id:
            raise KeyError(fid)
        by_id[fid].update(patch)
        by_id[fid]["retrieved_on"] = REVIEWED
    existing = set(by_id)
    for fw in NEW_FRAMEWORKS:
        if fw["framework_id"] in existing:
            # update in place
            by_id[fw["framework_id"]].update(fw)
        else:
            src["frameworks"].append(deepcopy(fw))
    src["generated_on"] = REVIEWED
    src["framework_count"] = len(src["frameworks"])


def patch_atlas(atlas: dict) -> None:
    existing = {m["mapping_id"] for m in atlas["mappings"]}
    # Upgrade / replace NOT_YET_MAPPED placeholders for ZA/JP
    replace = {
        "MAP-CAPS-NYM": "MAP-CAPS-SCI-ADJ",
        "MAP-ZA-CODING-NYM": "MAP-ZA-CODING-ADJ",
        "MAP-JP-COS-NYM": "MAP-JP-COS-ICT-ADJ",
    }
    atlas["mappings"] = [
        m for m in atlas["mappings"] if m["mapping_id"] not in replace
    ]
    for m in NEW_MAPPINGS:
        if m["mapping_id"] in existing and m["mapping_id"] not in replace.values():
            # refresh
            for i, old in enumerate(atlas["mappings"]):
                if old["mapping_id"] == m["mapping_id"]:
                    atlas["mappings"][i] = deepcopy(m)
                    break
        else:
            atlas["mappings"].append(deepcopy(m))
    # also refresh MAP-AC-DT-KE fidelity note if still PROPOSED — leave; we add ADJ sibling
    atlas["generated_on"] = REVIEWED
    atlas["mapping_count"] = len(atlas["mappings"])


def write_regional(jurisdictions: list[dict]) -> None:
    priority = {
        "africa": (
            "Track 2C: South Africa CAPS + Coding/Robotics deepened; Kenya BECF verified; "
            "Francophone/Lusophone/Arabic rows set TRANSLATION_REQUIRED where portals exist; "
            "ACCESS_BLOCKED only where public corpus unavailable."
        ),
        "middle_east": (
            "Track 2C: Bahrain NCF portal pinned; Gulf/Levant rows IDENTIFIED or TRANSLATION_REQUIRED; "
            "Syria/Yemen ACCESS_BLOCKED (conflict-era access)."
        ),
        "asia_pacific": (
            "Track 2C: AU/NZ/IN/SG/JP mandatory baselines deepened; ASEAN (ID/MY/PH) frameworks pinned; "
            "Pacific islands IDENTIFIED at portal level; conflict/closed systems ACCESS_BLOCKED."
        ),
        "americas": None,
        "europe": None,
        "global": None,
    }
    by_region: dict[str, list] = {}
    for j in jurisdictions:
        if j["level"] == "transnational":
            continue
        by_region.setdefault(j["region"], []).append(
            {
                "jurisdiction_id": j["jurisdiction_id"],
                "name": j["name"],
                "level": j["level"],
                "research_status": j["research_status"],
                "framework_ids": j.get("framework_ids") or [],
            }
        )
    for region, rows in by_region.items():
        if region not in ("africa", "middle_east", "asia_pacific"):
            # still refresh slices for consistency of counts if file exists
            pass
        counts = Counter(r["research_status"] for r in rows)
        note = priority.get(region)
        if note is None:
            # preserve existing priority_notes if we can
            path = STANDARDS / "regional" / f"{region}.yaml"
            old_note = ""
            if path.is_file():
                old = load_yaml(path)
                old_note = old.get("priority_notes") or ""
            note = old_note
        dump_yaml(
            STANDARDS / "regional" / f"{region}.yaml",
            {
                "schema": "kids.standards.regional/v1",
                "region": region,
                "generated_on": REVIEWED,
                "track_status": "DRAFT_INTERNAL",
                "jurisdiction_count": len(rows),
                "status_counts": dict(counts),
                "priority_notes": note,
                "jurisdictions": rows,
            },
        )


def write_coverage(jur: dict, src: dict, atlas: dict, before: dict, after: dict) -> None:
    jurisdictions = jur["jurisdictions"]
    sources = src["frameworks"]
    maps = atlas["mappings"]
    j_counts = Counter(j["research_status"] for j in jurisdictions)
    m_counts = Counter(m["fidelity"] for m in maps)
    mandatory = [s for s in sources if s.get("mandatory_baseline")]

    def fmt_counter(c: Counter) -> str:
        return ", ".join(f"{k}={v}" for k, v in sorted(c.items()))

    lines = [
        "# Global Standards Coverage Report",
        "",
        f"**Generated:** {REVIEWED}  ",
        "**Track status:** `DRAFT_INTERNAL` (not PUBLICATION_READY)  ",
        "**Schema:** `kids/standards/STANDARD_MAPPING_SCHEMA.md`  ",
        "**Track 2C:** Africa + Middle East + Asia-Pacific exhaustive research (PR #7)  ",
        f"**Accepted main (at branch base):** `82284cd8f41d750ff508cd6ea5bad0a9534d8162`",
        "",
        "## Jurisdiction metrics",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Jurisdictions total | {len(jurisdictions)} |",
        f"| OFFICIAL_VERIFIED | {j_counts.get('OFFICIAL_VERIFIED', 0)} |",
        f"| IDENTIFIED | {j_counts.get('IDENTIFIED', 0)} |",
        f"| TRANSLATION_REQUIRED | {j_counts.get('TRANSLATION_REQUIRED', 0)} |",
        f"| ACCESS_BLOCKED | {j_counts.get('ACCESS_BLOCKED', 0)} |",
        f"| NOT_YET_RESEARCHED | {j_counts.get('NOT_YET_RESEARCHED', 0)} |",
        "",
        "## Track 2C region before → after",
        "",
        "| Region | Before | After |",
        "| --- | --- | --- |",
    ]
    for region in ("africa", "middle_east", "asia_pacific"):
        lines.append(
            f"| {region} | {fmt_counter(before[region])} | {fmt_counter(after[region])} |"
        )
    lines.extend(
        [
            "",
            "## Mapping metrics",
            "",
            "| Fidelity | Count |",
            "| --- | ---: |",
            f"| EXACT | {m_counts.get('EXACT', 0)} |",
            f"| ADJACENT | {m_counts.get('ADJACENT', 0)} |",
            f"| PROPOSED | {m_counts.get('PROPOSED', 0)} |",
            f"| NO_MAP | {m_counts.get('NO_MAP', 0)} |",
            f"| NOT_YET_MAPPED | {m_counts.get('NOT_YET_MAPPED', 0)} |",
            f"| **Mappings total** | **{len(maps)}** |",
            "",
            "## Mandatory framework baseline status",
            "",
            "| Framework | Authority | Version | Verification | URL | Gaps |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for s in mandatory:
        gaps = "; ".join(s.get("gaps") or []) or "—"
        lines.append(
            f"| {s['title']} | {s['authority']} | {s.get('version')} | `{s.get('verification')}` | {s.get('url')} | {gaps} |"
        )
    lines.extend(
        [
            "",
            "## Honest gaps (priority)",
            "",
            "1. **Track 2C AFR/ME/APAC:** No remaining `NOT_YET_RESEARCHED` national rows in these three regions after this pass.",
            "2. **TRANSLATION_REQUIRED:** Large Francophone/Lusophone/Arabic/CJK queues — portals identified; clause maps blocked on language review.",
            "3. **ACCESS_BLOCKED:** Eritrea, Somalia, Syria, Yemen, Afghanistan, Myanmar, DPRK — public corpus unavailable or unreliable.",
            "4. **Japan / Indonesia / Malaysia / Thailand / Viet Nam / China / Korea:** Official instruments pinned; deep fidelity upgrades need translation.",
            "5. **South Africa Coding & Robotics:** Portal + draft/phase docs verified; prefer final gazetted phase PDFs when published.",
            "6. **NZ Te Mātaiaho:** Draft (Oct 2025) — NZC 2007 remains required until Gazette notice.",
            "7. **Americas / Europe:** Outside Track 2C scope; many rows may remain `NOT_YET_RESEARCHED`.",
            "8. **No EXACT maps:** Editorial grain uses `ADJACENT`/`PROPOSED`/`INFORMED_BY` only.",
            "9. **Copyright:** No wholesale standards text; domain-family summaries only.",
            "",
            "## Non-claims",
            "",
            "- Crosswalks are `CROSSWALKED_AGAINST` / `MAPPED_TO` / `INFORMED_BY` — **not** official alignment or certification.",
            "- Presence of a jurisdiction row ≠ completed clause-level mapping.",
            "- This track does not advance Gate 3 or PUBLICATION_READY counts.",
            "",
        ]
    )
    (STANDARDS / "GLOBAL_STANDARDS_COVERAGE_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    jur = load_yaml(STANDARDS / "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml")
    src = load_yaml(STANDARDS / "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml")
    atlas = load_yaml(STANDARDS / "GLOBAL_STANDARDS_ATLAS.yaml")

    before, after = patch_jurisdictions(jur)
    patch_sources(src)
    patch_atlas(atlas)

    dump_yaml(STANDARDS / "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml", jur)
    dump_yaml(STANDARDS / "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml", src)
    dump_yaml(STANDARDS / "GLOBAL_STANDARDS_ATLAS.yaml", atlas)
    write_regional(jur["jurisdictions"])
    write_coverage(jur, src, atlas, before, after)

    print("=== Track 2C BEFORE ===")
    for r, c in before.items():
        print(f"  {r}: {dict(c)}")
    print("=== Track 2C AFTER ===")
    for r, c in after.items():
        print(f"  {r}: {dict(c)}")
    # remaining NOT_YET in scope
    leftover = [
        j
        for j in jur["jurisdictions"]
        if j.get("region") in ("africa", "middle_east", "asia_pacific")
        and j.get("research_status") == "NOT_YET_RESEARCHED"
    ]
    print(f"Remaining NOT_YET in AFR/ME/APAC: {len(leftover)}")
    for j in leftover:
        print(f"  {j['jurisdiction_id']} {j['name']}")


if __name__ == "__main__":
    main()
