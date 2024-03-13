user_prompt_generator = """
You have an important role in an application that personalizes an experience for a specific user.

Your role within the greater system of the application is to generate {N} sets of binary prompting questions that will elicit the maximum amount of new information about the genuine interests of the user given what we currently do and do not know about the user.

The way that we learn more about the user is by presenting them with two reasonably different variations on a unifying concept, where the user's decision will be maximally informative about their unique topical and general interests; motivations; personality; and goals.

Your job is to generate these {N} sets of two options.

Here is what we already know about the user's unique topical and general interests; motivations; personality; and goals:
PROFILE:
{PROFILE}

Here are up to six interests that the user indicated from a comprehensive dropdown of themes/possible interests:
{INTERESTS}
(Do not pigeonhole them into ONLY asking questions about these topics, but use this a rough starting point for what they are drawn towards. Also, do not try to always synthesize all these topics in your prompts. Isolate them intelligently to learn as much as possible with each binary set of questions.

This session will consist of {N} question choices, so cover the relevant space accordingly!

Your CRITICAL job is to come up with a {N} binary prompting questions that will maximally contribute to refining and expanding the above PROFILE of the user's unique topical and general interests; motivations; personality; and goals.

Watch out for exploration vs. exploitation. Do NOT get stuck pigeon-holing the user/only deepening existing models/ideas/themes. ALSO BE EXPLORATORY! Accordingly, here were the last choices you presented the user:
{LAST_OPTIONS}

Make sure to not only deepen existing models (eg, the user is interested in X. Let's see if they're more interested in X.A or X.B) but also attempt to build NEW ones (eg, the user is interested in X. let's find out if they're also interested in Y). In other words, do BOTH of these in every round of question sets!
However, also note that if a user consistently indicates disinterest in a particular topic, do NOT keep pushing them on that topic! Learn from it and move on. We have a very finite number of questions to learn as much as possible. Waste none.

The choice will be presented to the user as 'which of these questions do you find more interesting?' followed by the options you give.

FORMATTING REQUIREMENTS: your output should contain two key parts: one 'REASONING:' section, followed by {N} binary prompting questions ('QUESTIONS:'). Each prompt should be preceded EXACTLY with the string (A) or (B) (see below for examples)

1. REASONING: given the PROFILE, reason ONCE succinctly but highly intelligently about what we still need to learn, and what general kinds of questions might elicit this new learning. 
1a. MAXIMIZE COVERAGE OF THE CONCEPTUAL SPACE. BE EXPLORATORY! EACH SESSION PROMPT PAIRING SHOULD AIM TO TEACH US SOMETHING FUNDAMENTALLY NEW ABOUT THE USER. DO NOT OVEREXPLOIT ON ALREADY-KNOWN INFORMATION/IDEAS/THEMES/TOPICS, BUT DO ZOOM INTO THESE AS WELL!
1b. Make sure the reasoning explicitly touches on what we hope to elicit/what general dichotomies we might want to probe using the impending set of paired question choices. (eg, abstract vs. concrete, realistic vs fantastical, etc). 
2. QUESTIONS: given REASONING, output the {N} sets of binary question sets that the user will select from. 
2a. Always include the 'QUESTIONS:' string before each set of prompts. Do NOT frame the questions as a 'would you rather' style choice or add any language like this. Simply generate two interesting questions. Separately, the user will be asked which they find more interesting (see good examples below).
2b. Do not include any sort of 'or' language WITHIN questions (A) or (B). Simply ask a question (see good examples below).

Pay general attention to this exemplar output, but do NOT overfit to the specific example given! It's just one possible example of very many.

EXAMPLAR OUTPUT (for N=3, note that REASONING ALWAYS HAPPENS EXACTLY ONCE, REGARDLESS OF N):
REASONING: Based on the user's demonstrated interest in technology and its creative applications, we have a solid understanding of their enthusiasm for innovation and its societal impacts. However, to gain a more holistic view of the user's interests and potential hidden passions, it's crucial to explore beyond the confines of technology. This exploration will help us identify other domains the user might find compelling, such as arts, psychology, or even philosophy. By juxtaposing a technology-focused question with one from a completely different field, we aim to uncover new layers of the user's interests, possibly revealing unexpected passions or curiosity areas that haven't been previously addressed.

QUESTIONS:
(A) Imagine you have the ability to create a new piece of technology that solves a personal inconvenience. What would this technology do, and how would it integrate into your daily life?
(B) Envision a project that uses technology to address a widespread societal challenge. What challenge would you focus on, and what would your solution entail?

QUESTIONS:
(A) If you were to start a creative hobby that also serves a community purpose, what would it be and how would you engage others?
(B) Consider the impact of creating a public art installation that incorporates interactive technology. What message or experience would you aim to convey?

QUESTIONS:
(A) Propose an idea for a novel or story that explores the theme of technology altering human relationships. What central conflict or question would you examine?
(B) How would you design an experiment or study to investigate the effects of virtual reality on empathy and social skills?

QUESTIONS:
(A) If you could delve into the study of an ancient civilization, which one would it be and what mystery or aspect of their society are you most interested in uncovering?
(B) Imagine you have the opportunity to learn an uncommon, perhaps even endangered, language fluently. Which language would you choose, and how do you think this knowledge could impact your perspective on the world or contribute to preserving cultural heritage?

YOUR OUTPUTS:
"""

infer_from_answers = """
You have an important role in an application that personalizes experiences for a specific user.

The user has just answered a set of binary question choices (the questions were generated by an AI) that were designed to elicit the maximum amount of new information about their interests, motivations, personality, and goals user given what we currently do and do not know about the user.

The reasoning behind these choices, the choices themselves, and the user's response to these choices was as follows (SESSION CHOICES):
{SESSION_CHOICES}

Your job is to make valid inferences about what can be reasonably inferred about the user's interests, motivations, personality, and goals from these choices. This is a bit subtle:
ABSOLUTELY CRITICAL POINT (MOST COMMON MISTAKE TO AVOID): DO NOT attribute to the user ANY specific topical interests that were introduced in the text of the SESSION CHOICES. It is critical to note that these options were written by the AI, not the user, so it is an error to say the user is interested in this or that SPECIFIC topic. Make VALID and GENERAL inferences about their interests given their choices!

Again, just because the user selects (A), for example, does not mean they are necessarily intrinsically interested in (A) in an absolute sense, but rather, are RELATIVELY MORE interested in (A) than (B). Make valid and conservative inferences given this subtle point, and do not overattribute interests to the user unless you see a clear pattern. 
CRITICAL: the key inference is NOT "why did the user select (X)? [--> they must be interested in X]" but rather, "what can we infer from the fact that the user selected (X) INSTEAD OF (Y)? What kind of person would select (X) over (Y)?" THIS IS A CRITICAL DISTINCTION TO UNDERSTAND!

Your outputs will be directlt passed to another person, who will use this information to update the running profile that we are building from the user. 

FORMATTING REQUIREMENTS: return the top five most important valid inferences that can be made from this information that is relevant for updating the user's profile. Order your outputs in order of most important/insightful/useful takeaways to potentially less insightful takeaways. Feel free to label key takeaways explicitly. Keep outputs rich and informative, but not needlessly verbose.

YOUR OUTPUTS:
"""

infer_from_answers_WITH_D = """
You have an important role in an application that personalizes experiences for a specific user.

The user has just answered a set of binary question choices (the questions were generated by an AI) that were designed to elicit the maximum amount of new information about their interests, motivations, personality, and goals user given what we currently do and do not know about the user.

The reasoning behind these choices, the choices themselves, and the user's response to these choices was as follows (SESSION CHOICES):
{SESSION_CHOICES}

Your job is to make valid inferences about what can be reasonably inferred about the user's interests, motivations, personality, and goals from these choices. This is a bit subtle:
CRITICAL POINT 1 (MOST COMMON MISTAKE TO AVOID): DO NOT attribute to the user ANY specific topical interests that were introduced in the text of the SESSION CHOICES. It is critical to note that these options were written by the AI, not the user, so it is an error to say the user is interested in this or that SPECIFIC topic. Make VALID and GENERAL inferences about their interests given their choices!
CRITICAL POINT 2: please pay particular attention if the user ever chose '(D) Neither/something else,' as this means they were sufficiently uninterested in options (A)/(B) and/or sufficiently interested in what they input here that they manually entered it. It IS okay to use these as specific topical interests that the user has (in contrast to CRITICAL POINT 1).

Again, just because the user selects (A), for example, does not mean they are necessarily intrinsically interested in (A) in an absolute sense, but rather, are RELATIVELY MORE interested in (A) than (B). Make valid and conservative inferences given this subtle point, and do not overattribute interests to the user unless you see a clear pattern. 
CRITICAL: the key inference is NOT "why did the user select (X)? [--> they must be interested in X]" but rather, "what can we infer from the fact that the user selected (X) INSTEAD OF (Y)? What kind of person would select (X) over (Y)?" THIS IS A CRITICAL DISTINCTION TO UNDERSTAND!

Your outputs will be directlt passed to another person, who will use this information to update the running profile that we are building from the user. 

FORMATTING REQUIREMENTS: return the top five most important valid inferences that can be made from this information that is relevant for updating the user's profile. Order your outputs in order of most important/insightful/useful takeaways to potentially less insightful takeaways. Feel free to label key takeaways explicitly. Keep outputs rich and informative, but not needlessly verbose.

YOUR OUTPUTS:
"""

profile_reconciliation = """
You have an important role in an application that personalizes experiences for a specific user.

The current model of the user's interests; motivations; personality; and goals is as follows (PROFILE):
{PROFILE}

And here are up to six interests that the user indicated from a comprehensive dropdown of themes/possible interests (INTERESTS):
{INTERESTS}

The user has just answered a set of binary question choices (content generated by AI) that were designed to elicit the maximum amount of new information about their interests, motivations, personality, and goals user given what we currently do and do not know about the user.

Here are the key insights that another person was able to extract from these latest choices (INSIGHTS), ordered from most to least important:
{INSIGHTS}

YOUR JOB IS TO RECONCILE THE CURRENT STATE OF THE PROFILE WITH THESE INSIGHTS. 
This may involve any of the following changes:
(1) Creating the profile from scratch if this is was their first session. If so, format the new profile as a set of succinct but maximally informative bullets, and be sure to integrate in the INTERESTS listed above, as the user explicitly shared these.
(2) Overwriting outdated information from the PROFILE that does not harmonize with the information gained from the new INSIGHTS.
(3) Adding new information into the PROFILE that is novel and currently not present given the information gained from the new INSIGHTS.
(4) Qualifying, refining, underscoring, or synthesizing content from the PROFILE with the information gained from the new INSIGHTS.

CRITICAL CONTEXT: the profile you output will be used to personalize a process for the user. It should grow over time to contain valuable information about the user's unique interests; motivations; personality; and deeper goals.

GENERALIZE THE INSIGHTS:
You may see information from the INSIGHTS such as: 'the user shows a preference for practical application of theoretical knowledge, as seen in their interest in creating technology to enhance mental well-being and in applying psychology to create empathetic virtual reality experiences.' 
HOWEVER, WE WANT TO ELIMINATE QUESTION-SPECIFIC DETAILS FROM THE PROFILE. Accordingly, this information might be MODIFIED as follows for the PROFILE: 'user shows a preference for practical application of theoretical knowledge, potentially to aid people at the intersection of psychology and advanced technology.'
IN THIS WAY, WE SCRUB OVERLY ESOTERIC INFORMATION FROM THE QUESTIONS AND JUST KEEP THE MORE GENERAL INSIGHT ABOUT THE USER FOR THE PROFILE. BE VERY DISCERNING ABOUT THE BALANCE BETWEEN SCRUBBING NEEDLESSLY DETAILED INFORMATION WHILE NOT ELIMINATING ANY POTENTIALLY VALUABLE INFORMATION.
The motivaton here is to not overattribute interests to the user from question text that the AI came up with, while still extracting all the valuable and generally informative pieces of information.
CRUCIAL EXCEPTION TO THIS RULE: If the INSIGHTS clearly indicate that the user EXPLICITLY/ACTIVELY indicated an interest (they may have written it in), you MUST include this information in the profile and DO NOT GENERALIZE IT in the way just described.

FORMATTING REQUIREMENTS:
- if this is the first time the profile is being generated, abide the the guidelines outlined in (1) above.
- make sure the INTERESTS always make it into the profile
- do not add any text above or below the bullets; it should just be the bullets
- if the profile already exists, ensure that the overall formatting of the profile remains the same after your revisions/additions.
- NEVER let the profile grow to more than a few hundred words/more than 8 key ideas/bullets. The bullets can grow in length past this, but NOT IN NUMBER!
- ALWAYS intelligently systematize/synthesize/cluster the profile rather than just continue listing every new insight or facet. Synthesize intelligently across sessions!

YOUR OUTPUTS:
"""

answer_profile_reconciliation = """
You have an important role in an application that personalizes experiences for a specific user.

The current model of the user's interests; motivations; personality; and goals is as follows (PROFILE):
{PROFILE}

And here are up to six interests that the user indicated from a comprehensive dropdown of themes/possible interests (INTERESTS):
{INTERESTS}

The user has just answered a set of binary question choices (content generated by AI) that were designed to elicit the maximum amount of new information about their interests, motivations, personality, and goals user given what we currently do and do not know about the user.

The reasoning behind these choices, the choices themselves, and the user's response to these choices was as follows (SESSION CHOICES):
{SESSION_CHOICES}
CRITICAL POINT 1 (YOUR MOST COMMON MISTAKE TO AVOID): DO NOT attribute to the user ANY specific topical interests that were introduced in the text of the SESSION CHOICES (these were introduced by the AI, not the user, so it is an error to say the user is interested in this or that SPECIFIC topic). Make VALID and GENERAL inferences about their interests given their choices!
CRITICAL POINT 2: please pay particular attention if the user ever chose '(D) Neither/something else,' as this means they were sufficiently uninterested in options (A)/(B) and/or sufficiently interested in what they input here that they manually entered it. It IS okay to use these as specific topical interests that the user has (in contrast to CRITICAL POINT 1).

Please update the PROFILE given the new SESSION CHOICES. This may involve any of the following changes:
(1) Creating the profile from scratch if this is was their first session. If so, format the new profile as a set of succinct but maximally informative bullets, and be sure to integrate in the INTERESTS listed above, as the user explicitly shared these.
(2) Overwriting outdated information from the PROFILE that does not harmonize with the information gained from the new SESSION CHOICES.
(3) Adding new information into the PROFILE that is novel and currently not present given the information gained from the new SESSION CHOICES.
(4) Qualifying, refining, or synthesizing content from the PROFILE with the information gained from the new SESSION CHOICES.

CRITICAL CONTEXT: the profile you output will be used to personalize a process for the user. It should grow over time to contain valuable information about the user's unique interests; motivations; personality; and deeper goals.

FORMATTING REQUIREMENTS:
- if this is the first time the profile is being generated, abide the the guidelines outlined in (1) above.
- do not add any text above or below the bullets; it should just be the bullets
- DO NOT INCLUDE any SPECIFIC topics here unless they were EXPLICITLY and ACTIVELY written in by the user (recall CRITICAL POINT 1 and CRITICAL POINT 2 above). DO NOT OVERATTRIBUTE INTERESTS TO THE USER! IT IS THE CRITICAL MISTAKE TO AVOID!
- if the profile already exists, ensure that the overall formatting of the profile remains the same after your revisions/additions.
- NEVER let the profile grow to more than a few hundred words/more than 8 key ideas/bullets. The bullets can grow in length past this, but NOT IN NUMBER! Keep it rich and informative, but succinct! Synthesize intelligently across sessions!
- ALWAYS intelligently systematize/synthesize/cluster the profile rather than just continue listing every new insight or facet.

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

Here is the user's rough thoughts about a possible angle (YOU MUST ALWAYS INTEGRATE THIS INTO AT LEAST ONE OR TWO OF YOUR SUGGESTIONS IF THERE IS ANY CONTENT HERE):
{FIRST_THOUGHTS}

Given the profile and the assigned prompt/topic of interest, please provide suggestions for personalizing the topic/prompt for them, taking their rough ideas into some account.
Requirement 1: if this seems like an assigned prompt, you MUST make sure that your outputs still fulfill the broad requirement of the prompt/essay topic (such that if the student writes about your prompts, they will ALSO be fulfilling the assigned topic.) THIS IS CRITICAL!
Requirement 2: please try to AVOID using specific topical information in the profile, instead leveraging their more general interests, motivations, personality, and goals to personalize the topic/prompt.
Requirement 3: please do NOT try to overambitiously synthesize every point of the user's profile or interests into a single prompt. Each suggestion should draw on a SMALL but CONTEXTUALLY RELEVANT subset of the user's profile. Be incisive and deep with your suggestions, not shallow and attempting to fit their whole profile into the personalization.
Requirement 4: please do NOT overexploit on the specified interests (weight these lower); give significantly more weight to the user profile.
Requirement 5: ALWAYS integrate their thinking into at least one or two of your suggestions if they offered any rough thoughts.

CRITICAL: THIS IS A TOOL MEANT TO FACILTIATE THE USER'S CREATIVITY, NOT FOR YOU TO COME UP WITH IDEAS FOR THEM. DO NOT GIVE DETAILS ON HOW TO APPROACH THE WRITING, JUST PRESENT THE PERSONALIZED TOPICS OF INTEREST.

FORMATTTING REQUIREMENTS:
Output three relatively short, incisive, high-quality numbered QUESTIONS that would personalize the relevant topic and serve as a prompt for the user. Try to hit at different SINGLE angles with each of the questions.
Just output the numbered questions, no other outputs!

YOUR OUTPUTS:
"""


prompt_idea_generator = """
REQUEST ID {RANDOM}:

You have an important role in an application that personalizes the writing experience for a specific user.

Given a user's profile (developed through their selections of various binary question choices generated by an AI), your job is to suggest a writing prompt for them.

Here is the current model of the user's unique interests; motivations; personality; and goals:
{PROFILE}

And here are some additional topical interests the user explicitly shared:
{INTERESTS}

Given this information, please generate a single compelling and interesting prompt for them.
Address your outputs warmly and helpfully directly to the user (second-person), don't speak about them.

Do NOT try to incorporate all or most of their profile or interests into a single prompt. It is okay to pick a few if desired to synergize, but it is too messy to try to meld them all. Picking a small chunk of the profile/interests and generating an amazing prompt from it is better than trying to squeeze the whole profile/interests into one prompt.
Be wary of inferring highly specific topical interests from the user's profile. TAKE GREAT PAINS NOT TO overattribute any specific topical information in the profile to the user unless the profile says that the user explicitly specified a specific interest.

Formatting requirement: simply output a key question for the user to explore with some related subquestions (no more than 3 subsquestions total). It should be one (unlabeled) question with a maximum of three (unlabeled) subsquestion bullets under it.
CRITICAL: THIS IS A TOOL MEANT TO FACILTIATE THE USER'S CREATIVITY, NOT FOR YOU TO COME UP WITH IDEAS FOR THEM. DO NOT GIVE DETAILS ON HOW TO APPROACH THE QUESTION, JUST PRESENT IT AS DESCRIBED ABOVE.

YOUR OUTPUTS:
"""


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
