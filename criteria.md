# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

Written at Milestone 2, before I replaced the chunker. At that point my corpus
was 23 documents chunking into 26 pieces with TOP_K of 5, so every question
came back with roughly a fifth of the entire corpus attached. On those odds
most of my questions should hit, and the one I am leaving room for is "When do
small local employers hire summer interns?" — its answer is a single month
sitting inside a threaded reply, and my 800-character window already severs
three chunks mid-sentence, so a one-word answer is exactly the kind of thing
that lands on the wrong side of a cut. That is one question I expect to be
fragile, not a tolerance I am spreading across all five: if anything else
misses, the problem is retrieval and not bad luck.

> **Re-measured after Milestones 3 and 4.** Target unchanged at 4 of 5. The
> corpus is now 23 chunks and TOP_K is 3, so a question sees about an eighth of
> the corpus rather than a fifth — a harder bar than the one I argued for, not
> an easier one. The mid-sentence severing that made the internship question
> fragile no longer happens either; its answer now sits whole inside
> `thread_internship_timing.txt`. I am leaving the target where it is because I
> wrote it before I knew that, which is the point of writing it first.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document. A question
the gate refuses is not an answer and is not counted here — it has no chunks to
name a source from. Criterion 5 is where refusals get scored; this criterion is
scored over the questions that reached the model.

**Why this target:**

All five rather than four, because naming the source is not something I am
hoping the model infers. Two things in my pipeline push it. `build_prompt` in
generate.py labels every excerpt with `[from filename]` before it goes out, so
the filename is literally present in the prompt. And GROUNDING_INSTRUCTION
tells the model in as many words to name the document the answer came from,
using the filename given in the excerpt. When the information is in the prompt
and the instruction asks for it directly, anything less than all five is a
failure I would want to look at rather than a tolerance I should have budgeted.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**

The two groups did not overlap, and it was not close. My five in-scope
questions scored between 0.2869 and 0.4206. The five OUT_OF_SCOPE questions
scored between 0.7866 and 0.9299. That is a gap of roughly 0.37 with nothing
in it, so the 0.6 cutoff is not a fine judgement — it sits in open space, and
anywhere between about 0.45 and 0.75 would sort these ten questions the same
way.

> **Re-measured after Milestone 3.** Target and cutoff both unchanged. The
> in-scope five did not move at all, because none of those threads was ever
> split. Every out-of-scope distance went up: the floor rose from 0.7866 to
> 0.8280 and the range is now 0.8280–0.9517, because the junk fragments were
> what nonsense questions had been matching — a 2-character chunk means nothing
> and so sits a middling distance from everything. The gap widened from 0.3660
> to 0.4074 and the workable range is now about 0.45 to 0.8. Fixing chunking
> bought this criterion margin it did not have when I wrote it.

---

## 4. No chunk is cut mid-sentence

Every chunk reads as a complete thought: none begins or ends with a sentence
cut in half. Checked across all 26 chunks in the corpus, not a sample of five.

**Why this target:**

Three of my 26 chunks currently fail this. One is the two-character fragment
`t.`. One begins `nd it's the only reason I got mine back after it was taken.`,
where the word `and` was severed mid-reply. The third begins `) ---` — the tail
end of a vote-count marker, with the reply it belonged to in the previous
chunk. All three are the same failure: my 800-character window closes wherever
it happens to land, and in a corpus of threaded replies that is usually the
middle of somebody's sentence.

A useful check I found while measuring: the three chunks cut mid-sentence are
exactly the three shorter than 200 characters — the same three, not merely a
similar number. So a 200-character floor is a quick proxy I can run on the
whole corpus, while the sentence-boundary rule above is the thing I actually
care about.

> **Re-measured after Milestone 3.** Target unchanged; it is now checked across
> 23 chunks rather than 26, and none fail. Two things I had wrong above. The
> cause was not the window closing mid-sentence — no document in my corpus
> reaches 800 characters, so the window never fired. It was the stride:
> `fallback_split` advances `chunk_size - overlap` = 680, so the three
> documents between 681 and 800 characters each got a second window holding
> only their tail (793−680=113, 739−680=59, 682−680=2). And the 200-character
> proxy was a coincidence of that arithmetic, not a property of my corpus, so
> it is not a check I would rely on again. My replacement chunker splits on
> reply boundaries and never inside one, which is why this now holds by
> construction rather than by luck.

---

## 5. No in-scope question comes back refused

None of my 5 in-scope test questions comes back as a refusal. A question counts
as refused if the printed answer contains the phrase "don't have enough
information", whether that came from the gate or from the model.

**Why this target:**

My system can refuse in two different places and I only control one of them.
The gate refuses on distance, and my measured distances leave that in no doubt:
my five in-scope questions score between 0.2869 and 0.4206 against a cutoff of
0.6, while the five out-of-scope ones score 0.7866 and above. Nothing in-scope
is close to the cutoff, so the gate is not where this will break. The other
place is the model. GROUNDING_INSTRUCTION in generate.py tells it to say it
doesn't have enough information whenever the documents don't cover the
question, and that judgement is made by the model on whatever chunks it was
handed — so a question can clear the gate comfortably and still come back
refused, if the chunks talk around the answer instead of stating it. That is
the failure this criterion is watching for, and it is why the target is all
five rather than four: a refusal on a question my corpus genuinely covers is
never something I want to have budgeted for.

This does sit in tension with criterion 1, and I would rather name it than let
it pass. There I allow one retrieval miss, and the internship question is the
one I expect it on. If that miss happens, the model gets chunks that don't
contain the month, and by the rule above it should say so — which would take
this criterion down with it. I am keeping both targets as they are. If they
fail together, that is one problem at the chunking stage and not two, and the
run log will show it as the same question in both rows.

> **Re-measured after Milestones 3 and 4.** Target unchanged. The in-scope
> distances are the same (0.2869–0.4206); the out-of-scope five now start at
> 0.8280 rather than 0.7866, so the gate has more room than when I wrote this,
> not less. Two changes push on the model side instead. TOP_K is now 3, so the
> model sees three chunks rather than five — less material to talk around the
> answer with, but also fewer chances for the answer to be in there at all. And
> I added two rules to GROUNDING_INSTRUCTION in Milestone 4, one of which tells
> it to report disagreement between replies rather than pick a side. Neither
> changes what counts as a refusal here.

---
