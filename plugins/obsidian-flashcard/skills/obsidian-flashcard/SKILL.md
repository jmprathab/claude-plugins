---
name: obsidian-flashcard
description: Generates spaced repetition flashcards in Obsidian Spaced Repetition plugin format. Use this skill when the user asks to create flashcards, study cards, make cards for spaced repetition, convert notes to flashcards, generate quiz cards, set up review cards, create Anki-style cards in Obsidian, or mentions studying, memorization, or learning material. Also trigger when they want to format flashcards using :: or ::: or ? or ?? or cloze deletions with ==, or when they mention the Spaced Repetition plugin. Convert any learning material into well-structured flashcard format that works with Obsidian.
---

# Obsidian Flashcard Generator

Convert notes into flashcards that work with the Obsidian Spaced Repetition plugin. The goal is effective learning through spaced repetition—the more focused and clear each flashcard, the better the retention.

## Core Principles

**Why focused cards matter:** Spaced repetition algorithms work best when each card tests one specific piece of knowledge. Dense, multi-concept cards are harder to review and lead to inconsistent recall. Break complex information into smaller pieces—it might feel like more work upfront, but it leads to much better learning outcomes.

**Question clarity:** Ambiguous questions create frustration during review. Make questions specific enough that there's one clear answer. If you find yourself hedging ("it depends..."), split it into multiple cards for different scenarios.

**Answer completeness:** Answers should be concise but complete. Too brief and you lose context; too long and you're back to dense cards. Aim for just enough information to fully answer the question without extra fluff.

### Flashcard Format Rules

**1. Single-line Basic (Question::Answer)**
Use for simple fact-based questions with one-line answers.
```
* What is a computer?::An electronic device that processes data
* What does CPU stand for?::Central Processing Unit
```

**2. Single-line Reversed (Question:::Answer)**
Creates TWO flashcards—both directions. Use for bidirectional knowledge (terms, definitions, facts).
```
* Paris:::Capital of France
* H2O:::Water
* 1969:::Year of moon landing
```

**3. Multi-line Basic (Question ? Answer)**
For longer content requiring multiple lines. End with `+++`.
```
* What are the main components of a computer system?
?
* Input devices: Keyboard, Mouse
* Output devices: Monitor, Printer
* Processing unit: CPU
* Storage: Hard drive, Memory
+++
```

**4. Multi-line Reversed (Question ?? Answer)**
Creates TWO multi-line flashcards—both directions. End with `+++`.
```
* List three programming languages and their uses
??
* Python: Easy to learn, great for beginners
* JavaScript: Essential for web development
* Java: Popular for enterprise applications
+++
```

**5. Cloze Deletion Cards (Basic Single Cloze)**
Hide specific parts using `==` delimiters. End with `+++` on a new line.
```
* The first female prime minister of Australia was ==Julia Gillard==
+++
* Water boils at ==100°C== at sea level
+++
```

**6. Multiple Cloze Deletions**
Creates separate sibling cards—each hides one deletion while showing others.
```
* ==Mitochondria== produce ==ATP== in cells
+++
```
This creates TWO cards:
- Card 1: "Mitochondria produce [...] in cells"
- Card 2: "[...] produce ATP in cells"

**7. Simplified Clozes with Hints**
Add optional hints using `^[hint]` syntax.
```
* The ==Pacific==^[largest ocean] Ocean covers one-third of Earth
+++
* This ==note==^[a written record] demonstrates hint usage
+++
```

### Important Formatting Notes

**Cloze type consistency:** The Spaced Repetition plugin doesn't handle mixing Simplified and Classic cloze formats well in the same note—it can cause parsing errors. Stick to one cloze style per note (the examples here use Simplified format with `==` delimiters).

**Separators matter:** The plugin uses these delimiters to parse cards, so getting them right is essential:
- Single-line cards: `::` for one-way, `:::` for reversed (bidirectional)
- Multi-line cards: `?` for one-way, `??` for reversed
- End multi-line and cloze cards with `+++` on its own line

**Organization:** Tag sections with `#flashcards` or organize into flashcard-specific folders—this helps you filter and review cards more easily in Obsidian.

### Card Design Approach

**Mixing formats:** You can use different flashcard types (single-line, multi-line, cloze) in the same note—just don't mix Simplified and Classic cloze formats together.

**How cloze cards work:** Each `==hidden element==` creates a separate card. If you have three deletions, you get three sibling cards—each one hides a different element while showing the others. This helps build connections between concepts.

**Reversed cards behavior:** When you use `:::` or `??`, you get two cards (question→answer and answer→question). The plugin may bury the reverse card until the next day to avoid showing both versions immediately.

**Simplicity wins:** When facing a complex topic, resist the urge to cram everything into one card. Multiple simple cards beat one complicated card every time. Your future self (during review sessions) will thank you for keeping each card focused.

**Using hints wisely:** In cloze cards, hints (`^[like this]`) can provide helpful context without giving away the answer. Think of them as gentle nudges toward the right track.

### Learning Scenario Guidelines

Different types of content work best with different flashcard formats:

**Vocabulary and terms:** Reversed single-line cards (`:::`) work great because you want to recall in both directions—term to definition and definition to term.

**Historical facts and dates:** Basic cards (`::`) or cloze deletions work well. For dates, cloze can be nice: "The moon landing happened in ==1969=="

**Complex definitions:** Multi-line cards (`?`) let you break down concepts that have multiple components or aspects without cramming everything onto one line.

**Formulas and equations:** Cloze deletions shine here—you can hide different variables or values: "E===mc²=="

**Processes and procedures:** Multi-line cards help you structure sequential steps clearly, making it easier to recall the order.

### Workflow

When converting notes to flashcards:

1. **Identify what matters:** Look for key concepts, facts, and relationships worth memorizing
2. **Choose the right format:** Pick the flashcard type that best fits each piece of information (see Learning Scenario Guidelines below)
3. **Keep it focused:** Each card should test one clear idea
4. **Structure the output:** Put all flashcards in a `## Flashcards` section—this makes them easy to find and move around
5. **Double-check formatting:** Make sure delimiters are correct so the plugin can parse everything properly

The output should be ready to paste directly into an Obsidian note without any modifications needed.

## Examples

### Example 1: Simple Vocabulary
**Input Notes:**
```
Python is a high-level programming language known for its simplicity.
Java is widely used in enterprise applications.
JavaScript powers interactive web applications.
```

**Output Flashcards Section:**
```
## Flashcards

* Python:::High-level programming language known for simplicity
* Java:::Programming language widely used in enterprise applications
* JavaScript:::Language that powers interactive web applications
```

### Example 2: Complex Concept
**Input Notes:**
```
The water cycle has four main stages: evaporation, condensation, precipitation, and collection.
Evaporation occurs when water changes from liquid to gas due to heat.
Condensation happens when water vapor cools and becomes liquid droplets.
Precipitation is when water falls as rain, snow, or sleet.
Collection is when water gathers in oceans, lakes, and rivers.
```

**Output Flashcards Section:**
```
## Flashcards

* What are the four main stages of the water cycle?
?
1. Evaporation—water changes from liquid to gas due to heat
2. Condensation—water vapor cools and becomes liquid droplets
3. Precipitation—water falls as rain, snow, or sleet
4. Collection—water gathers in oceans, lakes, and rivers
+++

* What is evaporation in the water cycle?::Water changes from liquid to gas due to heat

* What is condensation in the water cycle?::Water vapor cools and becomes liquid droplets

* What is precipitation in the water cycle?::Water falls as rain, snow, or sleet

* What is collection in the water cycle?::Water gathers in oceans, lakes, and rivers
```

### Example 3: Cloze Deletion
**Input Notes:**
```
E=mc² is Einstein's mass-energy equivalence equation.
The speed of light is approximately 3×10⁸ m/s.
Photosynthesis converts light energy into chemical energy.
```

**Output Flashcards Section:**
```
## Flashcards

* Einstein's mass-energy equivalence equation is ==E=mc²==
+++

* The speed of light is approximately ==3×10⁸ m/s==
+++

* ==Photosynthesis==^[process in plants] converts ==light energy==^[from the sun] into ==chemical energy==
+++
```
