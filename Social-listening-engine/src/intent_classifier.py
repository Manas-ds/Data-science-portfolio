# we did 2 methods for the intent classifier
# 1. Rule-Based
# 2. Zero-Shot Classifer

#1. 
import re

# making a copy to avoid accidental issues in future
events2 = reloaded.copy()

#backing up current
events2["intent_label_prev"] = events2["intent_label"]
events2["intent_conf_prev"]  = events2["intent_conf"]

INTENT_RULE_VERSION = "rules_v1"

KW = {
    "question": [
        r"\?$", r"\bhow\b", r"\bwhy\b", r"\bwhat\b", r"\bwhen\b", r"\bwhere\b", r"\bwho\b",
        r"\bcan you\b", r"\bcould you\b", r"\bis it\b", r"\bare you\b", r"\bany update\b"
    ],
    "request": [
        r"\bplease\b", r"\bplz\b", r"\bkindly\b",
        r"\bneed\b", r"\bwant\b", r"\brequire\b",
        r"\bhelp\b", r"\bsend\b", r"\bshare\b", r"\bprovide\b",
        r"\brefund\b", r"\breturn\b", r"\breplace\b", r"\bcancel\b", r"\bexchange\b",
        r"\bfix\b", r"\bresolve\b"
    ],
    "complaint": [
        r"\bworst\b", r"\bterrible\b", r"\bbad\b", r"\bawful\b", r"\bpathetic\b",
        r"\blate\b", r"\bdelay\b", r"\bdelayed\b",
        r"\bnot working\b", r"\bbroken\b", r"\bscam\b", r"\bfraud\b",
        r"\brude\b", r"\bdisappointed\b", r"\bangry\b"
    ],
    "praise": [
        r"\blove\b", r"\bamazing\b", r"\bawesome\b", r"\bgreat\b", r"\bfantastic\b",
        r"\bthank(s| you)\b", r"\bexcellent\b", r"\bbrilliant\b", r"\bperfect\b"
    ],
}

PRIORITY = ["question", "request", "complaint", "praise"]
PATTERNS = {k: [re.compile(p, re.IGNORECASE) for p in v] for k, v in KW.items()}

def rule_intent(text: str):
    t = text or ""
    for cat in PRIORITY:
        hits = [p.pattern for p in PATTERNS[cat] if p.search(t)]
        if hits:
            conf = min(0.55 + 0.15 * len(hits), 0.95)
            return cat, conf, hits[:3]
    return "other", 0.40, []

tmp = events2["text_clean"].map(rule_intent)

events2["intent_rule_version"] = INTENT_RULE_VERSION
events2["intent_label_rule"]   = tmp.map(lambda x: x[0])
events2["intent_conf_rule"]    = tmp.map(lambda x: x[1])
events2["intent_reason_rule"]  = tmp.map(lambda x: x[2])

# setting final intent fields from rules
events2["intent_label"] = events2["intent_label_rule"]
events2["intent_conf"]  = events2["intent_conf_rule"]

# review flags
events2["needs_review"] = (events2["intent_conf"] < 0.55) | (events2["intent_label"] == "other")

print("Intent distribution (rules):")
print(events2["intent_label"].value_counts())

other_rate = (events2["intent_label"] == "other").mean()
print("Other rate %:", round(other_rate * 100, 2))

events2[["text_clean","intent_label","intent_conf","intent_reason_rule"]].sample(10, random_state=2)


# extended list of keywords


KW_ADD = {
  "complaint": [
    r"\bdoes(?:n'?t)? work\b",
    r"\bnot working\b",
    r"\bstopped working\b",
    r"\bkeeps (?:crashing|freezing|buffering)\b",
    r"\b(crash(?:ed|es)?|froze|freezing)\b",
    r"\bwon'?t (?:load|open|start|install|update)\b",
    r"\bcan'?t (?:log in|login|sign in|connect|access)\b",
    r"\bunable to (?:log in|login|sign in|connect|access)\b",
    r"\blogin (?:failed|issue|problem)\b",
    r"\b(?:error|err)\s?(?:code|message)\b",
    r"\bgetting an error\b",
    r"\bbug(?:gy)? as hell\b",
    r"\bglitch(?:y)?\b",
    r"\bso (?:annoying|frustrating)\b",
    r"\bthis is (?:annoying|frustrating)\b",
    r"\bwhat a joke\b",
    r"\bthis is ridiculous\b",
    r"\bunacceptable\b",
    r"\bdisappointed\b",
    r"\breally bummed\b",
    r"\bpissed off\b",
    r"\bwtf\b",
    r"\bbruh[, ]+this\b",
    r"\bthanks for nothing\b",
    r"\bfix (?:this|it)\b",
    r"\bplease fix (?:this|it)\b",
    r"\bstill waiting\b",
    r"\bno response\b",
    r"\bnever again\b",
    r"\bworst (?:service|support|experience)\b",
    r"\b(?:over)?charged\b",
    r"\bcharged twice\b",
    r"\bwhere is my (?:order|refund)\b",
    r"\brefund (?:me|please)\b",
    r"\bscam(?:med)?\b",
    r"\babsolute (?:trash|garbage)\b",
  ],

  "praise": [
    r"\bshoutout to\b",
    r"\bprops to\b",
    r"\bhats off\b",
    r"\bwell done\b",
    r"\bnailed it\b",
    r"\byou (?:guys|all) killed it\b",
    r"\bthat was awesome\b",
    r"\bthis is awesome\b",
    r"\bso (?:good|great|amazing)\b",
    r"\blove (?:this|it|that)\b",
    r"\babsolutely love\b",
    r"\bobsessed with\b",
    r"\bbig fan\b",
    r"\bmy favorite\b",
    r"\bcan'?t get enough\b",
    r"\bthank you so much\b",
    r"\bthanks a ton\b",
    r"\breally appreciate\b",
    r"\bappreciate (?:it|this)\b",
    r"\bmade my day\b",
    r"\bmade my week\b",
    r"\bso proud\b",
    r"\bproud supporter\b",
    r"\bso happy (?:with|about)\b",
    r"\blooks great\b",
    r"\bworks like a charm\b",
    r"\b10/10\b",
    r"\bhighly recommend\b",
    r"\bwould recommend\b",
    r"\bbest (?:ever|thing)\b",
    r"\bthe best\b",
    r"\blegend(?:ary)?\b",
    r"\bgoat(ed)?\b",
    r"\byou rock\b",
    r"\bkeep it up\b",
    r"\bthank you (?:guys|all)\b",
  ],

  "question": [
    r"\banyone know\b",
    r"\bdoes anyone know\b",
    r"\bcan someone\b",
    r"\bcan anybody\b",
    r"\bany idea\b",
    r"\bany updates?\b",
    r"\bany update\b",
    r"\bwhat'?s the update\b",
    r"\bwhat is going on\b",
    r"\bwhat happened\b",
    r"\bwhy is (?:this|it|that)\b",
    r"\bhow do i\b",
    r"\bhow to\b",
    r"\bwhere do i\b",
    r"\bwhere can i\b",
    r"\bwhere is (?:my|the)\b",
    r"\bwhen (?:is|are|will)\b",
    r"\bwhat time\b",
    r"\bwhat date\b",
    r"\bwho else\b",
    r"\bis this (?:normal|safe|legit)\b",
    r"\bshould i\b",
    r"\bdo you (?:have|know)\b",
    r"\bare you (?:guys|all)\b",
    r"\bcan i\b",
    r"\bdoes it\b",
    r"\bwill it\b",
    r"\bwhere to (?:buy|get|find)\b",
    r"\banyone else (?:having|getting)\b",
    r"\bam i the only one\b",
    r"\bhelp me understand\b",
    r"\bwhat does (?:this|that)\s+mean\b",
    r"\b(?:pls|please)\s+explain\b",
    r"\bquick question\b",
    r"\bserious question\b",
    r"\?\s*$",
  ],

  "request": [
    r"\bplease (?:help|advise|assist)\b",
    r"\bpls (?:help|advise|assist)\b",
    r"\bcan you (?:help|fix|check|confirm)\b",
    r"\bcould you (?:help|fix|check|confirm)\b",
    r"\bwould you (?:please\s+)?(?:help|fix|check)\b",
    r"\bneed (?:help|support)\b",
    r"\bi need (?:help|support)\b",
    r"\blooking for (?:help|advice|recommendations?)\b",
    r"\bcan someone (?:help|assist)\b",
    r"\banyone (?:able|free) to help\b",
    r"\bplease (?:reply|respond)\b",
    r"\bpls (?:reply|respond)\b",
    r"\bplease (?:dm|pm)\b",
    r"\bpls (?:dm|pm)\b",
    r"\bplease (?:send|share)\b",
    r"\bpls (?:send|share)\b",
    r"\bplease (?:look|check) into\b",
    r"\bcan you (?:send|share)\b",
    r"\bcould you (?:send|share)\b",
    r"\bcan you (?:recommend|suggest)\b",
    r"\bcould you (?:recommend|suggest)\b",
    r"\brecommend me\b",
    r"\bsuggest (?:me|some)\b",
    r"\bplease (?:add|include)\b",
    r"\bplease (?:remove|delete)\b",
    r"\bplease (?:cancel|pause)\b",
    r"\bplease (?:refund|replace)\b",
    r"\bpls (?:refund|replace)\b",
    r"\bfix this (?:please|pls)\b",
    r"\bhelp (?:me|us) out\b",
    r"\bdo me a favor\b",
    r"\bplease retweet\b",
    r"\bpls rt\b",
    r"\bcan you (?:RT|retweet)\b",
    r"\bfollow back\b",
    r"\bplease follow\b",
    r"\bcan you (?:follow|subscribe)\b",
  ],
}

# got the data from chatbot, i gave 300 texts, asked it do give me phrases and keywords

KW_ADD2 = {
  "conversation": [
    # personal narrative / setup
    r"\bso i was\b",
    r"\bso we were\b",
    r"\bso there i was\b",
    r"\byesterday i\b",
    r"\blast night i\b",
    r"\bthis morning i\b",
    r"\bthe other day\b",
    r"\btoday i (was|went|saw|heard|found|realized)\b",
    r"\bjust (got|saw|found|heard|realized)\b",
    r"\b(i|we) just (found out|realized|remembered)\b",
    r"\b(i|we) just (saw|heard|learned)\b",
    r"\bturns out\b",
    r"\bso apparently\b",
    r"\bplot twist\b",
    r"\bthat moment when\b",
    r"\bmeanwhile\b",
    r"\banyway[,!]\b",
    r"\blong story short\b",
    r"\btl;dr\b",
    r"\btrue story\b",
    r"\bstory time\b",

    # dialogue / retelling
    r"\b(i|we) (was|were) like\b",
    r"\b(i|we) (went|walked|drove) (to|into)\b",
    r"\bthen (he|she|they) (said|goes)\b",
    r"\bmy (friend|buddy|mom|dad|sister|brother|coworker|roommate) (said|was like)\b",
    r"\b(i|we) told (him|her|them)\b",
    r"\b(i|we) asked (him|her|them)\b",
    r"\".*\b(i|we)\b.*\"",

    # vibe / self-talk
    r"\bnot gonna lie\b",
    r"\bno joke\b",
    r"\bi swear\b",
    r"\bcan'?t stop (laughing|thinking)\b",
    r"\bwhat a (day|week)\b",
    r"\bmy (life|day) in a nutshell\b",
    r"\brandom thought\b",
    r"\bshower thought\b",
    r"\bguess what\b",
    r"\bmay or may not\b",
    r"\b(or )?may not\b",
    r"\bso i guess\b",

    # casual greetings / life updates
    r"\bhappy (birthday|bday|anniversary)\b",
    r"\bbelated happy birthday\b",
    r"\bhappy (friday|monday|tuesday|wednesday|thursday|saturday|sunday)\b",
    r"\bhow('?s| is) everyone (doing|today)\b",
    r"\bwhat are you (up to|doing) (today|tonight)\b",

    # light coordination / social chatter (not brand-action)
    r"\bwhos going to\b",
    r"\bwho's going to\b",
    r"\banyone going to\b",
    r"\bwe should (totally|totes)?\s*meet\b",
    r"\banyone else remember\b",
    r"\bremember when\b",
    r"\bcan we talk about\b",

    # common “sharing stuff”
    r"\b(i|we) added a (video|song)\b",
    r"\b(i|we) (got|added) a (video|pic|photo)\b",
    r"\bnew photo of\b",
    r"\blost & found\b",
    r"\brest in peace\b",
    r"\brip\b",
    r"\blooking forward to\b",
    r"\bcan'?t wait (to|for)\b",
  ],

  "sarcasm": [
    # classic sarcasm markers
    r"\byeah right\b",
    r"\bas if\b",
    r"\bsure jan\b",
    r"\blove that for me\b",
    r"\bmust be nice\b",
    r"\bthanks for nothing\b",
    r"\bthanks a lot\b",
    r"\bcool story bro\b",
    r"\bwhat could possibly go wrong\b",
    r"\bbecause of course\b",
    r"\bof course it (did|does|would)\b",

    # mock-positive templates
    r"\bgreat job\b",
    r"\bnice going\b",
    r"\bgood one\b",
    r"\bwell that'?s just great\b",
    r"\bkeep up the great work\b",
    r"\bjust what i needed\b",
    r"\bexactly what i wanted\b",
    r"\bhow (nice|lovely) of you\b",

    # “not” flips (high precision when paired)
    r"\bperfect\b.*\bnot\b",
    r"\bawesome\b.*\bnot\b",
    r"\bso helpful\b.*\bnot\b",
    r"\bthank you\b.*\bnot\b",
    r"\bappreciate it\b.*\bnot\b",
    r"\bworks like a charm\b.*\bnot\b",
    r"\bnailed it\b.*\bnot\b",
    r"\bgenius\b.*\bnot\b",
    r"\bbravo\b.*\bnot\b",
    r"\bwell played\b.*\bnot\b",

    # explicit sarcasm annotation
    r"\b\/s\b",
    r"\b\#sarcasm\b",
    r"\b(sarcasm|sarcastic)\b",

    # meme-y / internet sarcasm
    r"\bslow clap\b",
    r"\bclap clap\b",
    r"\bthanks captain obvious\b",
    r"\bbless your heart\b",
    r"\b10/10\b.*\brecommend\b",
    r"\bwhat a (surprise|shock)\b",
    r"\bshocking\b.*\bnot\b",

    # “yeah, sure” type (keep tight)
    r"\b(yeah|yea)\s+okay\b",
    r"\bokay[,!]*\s*sure\b",
    r"\bsuu+re\b",
    r"\brii+ght\b",
    r"\bright{2,}\b",

    # exaggerated blame / mock certainty
    r"\byeah[, ]+everything is\b.*\bfault\b",
    r"\beven if\b.*\b(it'?s|its)\s+gonna be\b.*\bfault\b",

    # sardonic consolation / backhanded framing
    r"\bon the bright side\b",
    r"\b(i guess|guess) i'll just\b",
    r"\b(i'?m|im) thrilled\b",
    r"\bcongrats\b.*\bnot\b",

    # “welcome back…don’t screw it up” style irony
    r"\bwelcome back\b.*\b(don'?t|dont)\s+(screw|mess)\s+it\s+up\b",
  ]
}


import numpy as np
import re

# --- rollback-friendly backup (do this once before overwriting) ---
events2["intent_label_prev"] = events2.get("intent_label", np.nan)
events2["intent_conf_prev"]  = events2.get("intent_conf", np.nan)
events2["needs_review_prev"] = events2.get("needs_review", np.nan)

# --- updated PRIORITY (includes new labels) ---
PRIORITY = ["sarcasm", "conversation", "request", "complaint", "question", "praise"]

# --- merge KW + KW_ADD + KW_ADD2 into one dict (dedup) ---
KW_ALL = {}
for k in set(list(KW.keys()) + list(KW_ADD.keys()) + list(KW_ADD2.keys())):
    combined = KW.get(k, []) + KW_ADD.get(k, []) + KW_ADD2.get(k, [])
    seen = set()
    KW_ALL[k] = [x for x in combined if not (x in seen or seen.add(x))]

# --- compile patterns once ---
PATTERNS = {k: [re.compile(p, re.IGNORECASE) for p in KW_ALL[k]] for k in KW_ALL}

def rule_intent(text: str):
    t = text or ""
    for cat in PRIORITY:
        hits = [p.pattern for p in PATTERNS.get(cat, []) if p.search(t)]
        if hits:
            conf = min(0.55 + 0.12 * len(hits), 0.95)
            return cat, conf, hits[:3]
    return "other", 0.40, []

tmp = events2["text_clean"].map(rule_intent)

events2["intent_rule_version"] = "rules_expanded_kw_add_kw_add2"
events2["intent_label_rule"]   = tmp.map(lambda x: x[0])
events2["intent_conf_rule"]    = tmp.map(lambda x: x[1])
events2["intent_reason_rule"]  = tmp.map(lambda x: x[2])

events2["intent_label"] = events2["intent_label_rule"]
events2["intent_conf"]  = events2["intent_conf_rule"]

events2["needs_review"] = (events2["intent_conf"] < 0.55) | (events2["intent_label"] == "other")

print("Intent distribution (expanded rules):")
print(events2["intent_label"].value_counts())

print("Other rate %:", round((events2["intent_label"] == "other").mean() * 100, 2))
print("conversation:", (events2["intent_label"] == "conversation").sum())
print("sarcasm:", (events2["intent_label"] == "sarcasm").sum())


## 2. 

from transformers import pipeline
import time


LABELS = ["complaint", "praise", "question", "request", "conversation", "sarcasm", "other"]

# Only used for fallback rows
CANDIDATE_LABELS = ["complaint", "praise", "question", "request", "conversation", "sarcasm"]

clf = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli",
    device=-1
)

def clip(s, n=200):
    s = s or ""
    return s[:n]

other_mask = events2["intent_label"] == "other"
todo_idx = events2[other_mask].index[:5000].tolist()  # demo-cap

batch_size = 2000
n_batches = (len(todo_idx) + batch_size - 1) // batch_size
print("Fallback rows:", len(todo_idx), "batches:", n_batches)

for b in range(n_batches):
    batch_idx = todo_idx[b*batch_size:(b+1)*batch_size]
    texts = events2.loc[batch_idx, "text_clean"].tolist()
    texts = [clip(t) for t in texts]

    t0 = time.time()
    preds = clf(texts, candidate_labels=CANDIDATE_LABELS, multi_label=False)

    events2.loc[batch_idx, "intent_label_zs"] = [p["labels"][0] for p in preds]
    events2.loc[batch_idx, "intent_conf_zs"]  = [p["scores"][0] for p in preds]
    print(f"Batch {b+1}/{n_batches} done in {time.time()-t0:.1f}s")

