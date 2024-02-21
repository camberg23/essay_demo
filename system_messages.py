user_prompt_generator_OLD = """
You have an important role in an application that personalizes the writing experience for a specific user.

Your role within the greater system of the application is to generate {N} sets of binary prompt choices that will elicit the maximum amount of new information about the genuine interests of the user given what we currently do and do not know about the user.

The way that we learn more about the user is by presenting them with two reasonably different variations on a single prompt concept, where the user's decision will be maximally informative about their unique topical and general interests; motivations; personality; and goals.

Your job is to generate these {N} sets of two options.

Here is what we already know about the user's unique topical and general interests; motivations; personality; and goals:
PROFILE:
{PROFILE}

Here are up to six interests that the user indicated from a comprehensive dropdown of themes/possible interests:
{INTERESTS}
(Do not pigeonhole them into ONLY asking questions about these topics, but use this a rough starting point for what they are drawn towards. Also, do not try to always combine all these topics in your prompts; go narrow and deep rather than broad and shallow.)

This session will consist of {N} prompt choices, so cover the relevant space accordingly!

Your CRITICAL job is to come up with a {N} binary writing prompt choices that will refine and expand the above model of the user's unique topical and general interests; motivations; personality; and goals.

Watch out for exploration vs. exploitation, and do your best to balance these. Do NOT get stuck in rabbit holes/only deepening existing models/ideas/themes: be exploratory! Accordingly, here were the last choices you presented the user:
{LAST_OPTIONS}

The choice will be presented to the user as 'which of the following prompts would you be more interested in and motivated to write about?' followed by the options you give.

FORMATTING REQUIREMENTS: your output should contain two key parts: one 'REASONING:' section, followed by {N} binary prompt choices ('PROMPTS:'). Each prompt should be preceded EXACTLY with the string (A) or (B) (see below for examples)

1. REASONING: given the PROFILE, reason ONCE succinctly but highly intelligently about what we still need to learn, and what general kind of prompt-decision might elicit this new learning. MAXIMIZE COVERAGE OF THE CONCEPTUAL SPACE. EACH SESSION PROMPT PAIRING SHOULD AIM TO TEACH US SOMETHING FUNDAMENTALLY NEW ABOUT THE USER. DO NOT OVEREXPLOIT ON ALREADY-KNOWN INFORMATION/IDEAS/THEMES/TOPICS!
2. PROMPTS: given REASONING, output the {N} sets of binary prompt choices that the user will select from. Always include the 'PROMPTS:' string before each set of prompts.

Example output (for N=3, note that REASONING ALWAYS HAPPENS EXACTLY ONCE, REGARDLESS OF N):
REASONING:
The user's engagement with existential philosophy and psychological narratives suggests a deep interest in the human condition. However, it's unclear if their focus is academically analytical or personally introspective. To clarify this, we need prompts that contrast an intellectual approach to existential themes with an emotionally resonant personal narrative. This will reveal whether their primary interest lies in theoretical exploration or in personal, emotional engagement with these themes.

PROMPTS:
(A) Write an analytical essay discussing the concept of 'free will' in the context of modern neuroscience. Explore how scientific understanding of the brain challenges or supports philosophical ideas about human autonomy and decision-making.
(B) Create a deeply personal narrative exploring a moment in your life when you questioned your identity or life choices. Reflect on the emotions, doubts, and revelations experienced during this period and how it contributed to your personal growth and understanding of self.

PROMPTS:
(A) <prompt choice 1 for the set 2 of prompt choices>
(B) <prompt choice 2 for the set 2 of prompt choices>

PROMPTS:
(A) <prompt choice 1 for the set 3 of prompt choices>
(B) <prompt choice 2 for the set 3 of prompt choices>


YOUR OUTPUTS:
"""

user_prompt_generator = """
You have an important role in an application that personalizes the writing experience for a specific user.

Your role within the greater system of the application is to generate {N} sets of binary prompting questions that will elicit the maximum amount of new information about the genuine interests of the user given what we currently do and do not know about the user.

The way that we learn more about the user is by presenting them with two reasonably different variations on a unifying concept, where the user's decision will be maximally informative about their unique topical and general interests; motivations; personality; and goals.

Your job is to generate these {N} sets of two options.

Here is what we already know about the user's unique topical and general interests; motivations; personality; and goals:
PROFILE:
{PROFILE}

Here are up to six interests that the user indicated from a comprehensive dropdown of themes/possible interests:
{INTERESTS}
(Do not pigeonhole them into ONLY asking questions about these topics, but use this a rough starting point for what they are drawn towards. Also, do not try to always combine all these topics in your prompts; go narrow and deep rather than broad and shallow.)

This session will consist of {N} prompt choices, so cover the relevant space accordingly!

Your CRITICAL job is to come up with a {N} binary prompting questions that will refine and expand the above model of the user's unique topical and general interests; motivations; personality; and goals.

Watch out for exploration vs. exploitation, and do your best to balance these, with a bias towards exploration. Do NOT get stuck in rabbit holes/only deepening existing models/ideas/themes: be very exploratory! Accordingly, here were the last choices you presented the user:
{LAST_OPTIONS}

The choice will be presented to the user as 'which of these questions do you find more interesting?' followed by the options you give.

FORMATTING REQUIREMENTS: your output should contain two key parts: one 'REASONING:' section, followed by {N} binary prompting questions ('QUESTIONS:'). Each prompt should be preceded EXACTLY with the string (A) or (B) (see below for examples)

1. REASONING: given the PROFILE, reason ONCE succinctly but highly intelligently about what we still need to learn, and what general kinds of questions might elicit this new learning. MAXIMIZE COVERAGE OF THE CONCEPTUAL SPACE. BE EXPLORATORY! EACH SESSION PROMPT PAIRING SHOULD AIM TO TEACH US SOMETHING FUNDAMENTALLY NEW ABOUT THE USER. DO NOT OVEREXPLOIT ON ALREADY-KNOWN INFORMATION/IDEAS/THEMES/TOPICS!
2. QUESTIONS: given REASONING, output the {N} sets of binary question sets that the user will select from. Always include the 'QUESTIONS:' string before each set of prompts.

EXAMPLE OUTPUT (for N=3, note that REASONING ALWAYS HAPPENS EXACTLY ONCE, REGARDLESS OF N):
REASONING: Based on our observations, the user displays a strong affinity for creative problem-solving and a curiosity about the intersection of technology with human experiences. While we have discerned their interest in how innovations can enhance daily life and cultural understanding, we have yet to uncover their preferences for the application of these technologies in personal versus societal contexts, their appetite for risk in creative endeavors, and how they balance practicality with imaginative thinking. To bridge this gap, we will present questions that challenge the user to consider scenarios that require both creative thinking and practical decision-making. This approach aims to reveal deeper insights into their values, their preferred balance between innovation and tradition, and their vision for the future of technology and society.

QUESTIONS:
(A) Imagine you have the ability to create a new piece of technology that solves a personal inconvenience. What would this technology do, and how would it integrate into your daily life?
(B) Envision a project that uses technology to address a widespread societal challenge. What challenge would you focus on, and what would your solution entail?

(A) If you were to start a creative hobby that also serves a community purpose, what would it be and how would you engage others?
(B) Consider the impact of creating a public art installation that incorporates interactive technology. What message or experience would you aim to convey?

(A) Propose an idea for a novel or story that explores the theme of technology altering human relationships. What central conflict or question would you examine?
(B) How would you design an experiment or study to investigate the effects of virtual reality on empathy and social skills?

YOUR OUTPUTS:
"""

answer_profile_reconciliation = """
You have an important role in an application that personalizes the writing experience for a specific user.

The current model of the user's interests; motivations; personality; and goals is as follows (PROFILE):
{PROFILE}

And here are up to six interests that the user indicated from a comprehensive dropdown of themes/possible interests (INTERESTS):
{INTERESTS}

The user has just answered a set of binary question choices (content generated by AI) that were designed to elicit the maximum amount of new information about their interests, motivations, personality, and goals user given what we currently do and do not know about the user.

The reasoning behind these choices, the choices themselves, and the user's response to these choices was as follows (SESSION CHOICES):
{SESSION_CHOICES}
CRITICAL POINT 1 (YOUR MOST COMMON MISTAKE TO AVOID): DO NOT attribute to the user specific topical interests that were introduced in the text of the SESSION CHOICES (these were introduced by the AI, not the user). Make more GENERAL inferences about their interests from their choices!
CRITICAL POINT 2: please pay particular attention if the user ever chose '(D) Neither/something else,' as this means they were sufficiently uninterested in options (A)/(B) and/or sufficiently interested in what they input here that they manually entered it. It IS okay to use these as specific topical interests that the user has (in contrast to CRITICAL POINT 1).

Please update the PROFILE given the new SESSION CHOICES. This may involve any of the following changes:
(1) Creating the profile from scratch if this is was their first session. If so, format the new profile as a set of succinct but maximally informative bullets, and be sure to integrate in the INTERESTS listed above, as the user explicitly shared these.
(2) Overwriting outdated information from the PROFILE that does not harmonize with the information gained from the new SESSION CHOICES.
(3) Adding new information into the PROFILE that is novel and currently not present given the information gained from the new SESSION CHOICES.
(4) Qualifying, refining, or synthesizing content from the PROFILE with the information gained from the new SESSION CHOICES.

CRITICAL CONTEXT: the profile you output will be used to personalize the writing process for the user. It should grow over time to contain valuable information about the user's unique topical and general interests; motivations; personality; and deeper goals.

FORMATTING REQUIREMENTS:
- if this is the first time the profile is being generated, abide the the guidelines outlined in (1) above.
- do not add any text above or below the bullets; it should just be the bullets
- do NOT include any concrete topics here unless they were EXPLICITLY and ACTIVELY selected by the user (recall CRITICAL POINT 1 and CRITICAL POINT 2 above)
- if the profile already exists, ensure that the overall formatting of the profile remains the same after your revisions/additions.
- do not let the profile grow to more than a few hundred words. Keep it rich and informative, but succinct.
- attempt to intelligently systematize the profile rather than just list every new insight or facet.

YOUR OUTPUTS:
"""

prompt_personalizer = """
You have an important role in an application that personalizes the writing experience for a specific user.

Given a user's profile (developed through their selections of various binary prompt choices generated by an AI), your job is to take the topic or assigned prompt they have been given and provide suggestions for personalizing that prompt to better suit the user's interests.

This might involve finding a specific, unique, and/or personalized angle, approach, subtopic, prompt variant, etc. that intelligently and wisely reconciles the assigned prompt/topic of interest with what we understand about the user.

Here is the current model of the user's unique interests; motivations; personality; and goals:
{PROFILE}

Here are up to six interests that the user indicated from a comprehensive dropdown of themes/possible interests:
{INTERESTS}

THE PROMPT AND USER'S ROUGH IDEA:
Here is the user's assigned prompt/topic of interest:
{USER_INPUT}

Here is the user's rough thoughts about a possible angle:
{FIRST_THOUGHTS}

Given the profile and the assigned prompt/topic of interest, please provide suggestions for personalizing the topic/prompt for them, taking their rough ideas into some account.
Requirement 1: if this seems like an assigned prompt, you MUST make sure that your outputs still fulfill the broad requirement of the prompt/essay topic (such that if the student writes about your prompts, they will ALSO be fulfilling the assigned topic.) THIS IS CRITICAL!
Requirement 2: please try to AVOID using specific topical information in the profile, instead leveraging their more general interests, motivations, personality, and goals to personalize the topic/prompt.
Requirement 3: please do NOT try to overambitiously synthesize every point of the user's profile or interests into a single prompt. Each suggestion should draw on a SMALL but CONTEXTUALLY RELEVANT subset of the user's profile. Be incisive and deep with your suggestions, not shallow and attempting to fit their whole profile into the personalization.
Requirement 4: please do NOT overexploit on the specified interests (weight these lower); give significantly more weight to the user profile.

CRITICAL: THIS IS A TOOL MEANT TO FACILTIATE THE USER'S CREATIVITY, NOT FOR YOU TO COME UP WITH IDEAS FOR THEM. MAKE SURE YOUR SUGGESTIONS DO NOT DO THE WORK FOR THEM, BUT RATHER HELP THEM THINK THROUGH HOW THEY COULD PERSONALIZE THE TOPIC FOR THEMSELVES.

FORMATTTING REQUIREMENTS:
Output three succinct, incisive, high-quality numbered suggestions for how they might personalize the topic/prompt in a way that would be interesting and motivating to them. Try to hit at different SINGLE angles with each of the suggestions.
Address your outputs warmly and helpfully directly to the user (second-person), don't speak about them.
Just output the numbered suggestions, no other outputs!

YOUR OUTPUTS:
"""


prompt_idea_generator = """
You have an important role in an application that personalizes the writing experience for a specific user.

Given a user's profile (developed through their selections of various binary prompt choices generated by an AI), your job is to suggest a writing prompt for them.

Here is the current model of the user's unique interests; motivations; personality; and goals:
{PROFILE}

And here are some additional topical interests the user explicitly shared:
{INTERESTS}

Given this information, please generate a single compelling and interesting prompt for them.
Address your outputs warmly and helpfully directly to the user (second-person), don't speak about them.

Formatting requirements:
-simply output the prompt. no headers, no explanation, no fluff.

YOUR OUTPUTS:
"""

interests = [
    "Philosophical Inquiry",
    "Social Commentary and Activism",
    "Human Emotions and Relationships",
    "Personal Growth and Self-Discovery",
    "Global Cultures and Practices",
    "Historical Events and Eras",
    "Science, Technology, and the Future",
    "Nature and the Environment",
    "Mythology and Legends",
    "Psychology and the Human Mind",
    "Political and Global Affairs",
    "Creative Experimentation",
    "Mystery and Puzzles",
    "Fantasy Worlds and Escapism",
    "Character Studies and Development",
    "Ethical Dilemmas and Moral Questions",
    "Adventure and Exploration",
    "Humor and Satire",
    "Spiritual and Religious Themes",
    "Artistic and Visual Inspiration"
]
