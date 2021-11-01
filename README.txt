=================================================================================
  SemEval-2022 Task 9: R2VQ - Competence-based Multimodal Question Answering
            
James Pustejovsky (1), Jingxuan Tu (1), Marco Maru (2),
Simone Conia (2), Roberto Navigli (2), Kyeongmin Rim (1),
Kelley Lynch (1), Richard Brutti (1), Eben Holderness (1)

1) Brandeis University
2) Sapienza NLP Group, Sapienza University of Rome

           Codalab: https://competitions.codalab.org/competitions/34056                                                                                                                                                                     
=================================================================================


The Competence-based Multimodal Question Answering task is structured as question answering pairs, querying how well a system understands the semantics of recipes derived from a collection of cooking recipes and videos. Each question belongs to a "question family" reﬂecting a speciﬁc reasoning competence. The associated R2VQ dataset is designed for testing competence-based comprehension of machines over a multimodal recipe collection labeled according to three distinct annotation layers: (i) Cooking Role Labeling (CRL), (ii) Semantic Role Labeling (SRL), and (iii) aligned image frames taken from creative commons cooking videos downloaded from YouTube. It consists of 1,000 recipes, with 800 to be used as training, and 100 recipes each for validation and testing. Participating systems will be exposed to the aforementioned multimodal training set, and will be asked to provide answers to unseen queries exploiting (i) visual and textual information jointly, or (ii) textual information only.

Data and annotation information is detailed below.



=================================================================================
DATASET CONTENT
=================================================================================

The training folder (train) contains the following files:

```
README.txt        (this file)
LICENSE.txt       (describes under which conditions one can use the data)
train/
    crl_srl.csv       (recipes with CRL and SRL annotations + QA pairs)
    images/           (contains all the images for each recipe)
        f-2KJMRNHC/   (contains all the images for recipe with ID = f-2KJMRNHC)
            ...
        f-2SNBZJVX/   (contains all the images for recipe with ID = f-2SNBZJVX)
            ...
        ...
```

=================================================================================
DATA FORMAT
=================================================================================

= train/crl_srl.csv
This file format is adapted from the CoNLL-U format (https://universaldependencies.org/format.html).
It contains all the recipes (ingredients, steps, metadata, annotations).

== metadata
As usual in CoNLL-U files, lines starting with # are used to provide metadata.
For example:
# newdoc id = f-6VWP66LZ (indicates the ID of the following recipe)
...
# newpar id = f-6VWP66LZ::ingredients (following lines will indicate ingredients)
# sent_id = f-6VWP66LZ::ingredients::sent01 (first ingredient)
# text = 500g broccoli (original sentence describing the ingredient)
...
# newpar id = f-6VWP66LZ::step01 (first step of the recipe)
# sent_id = f-6VWP66LZ::step01::sent01 (first sentence of the first step)
# text = Cut the broccoli into flowerets [...] (original sentence for this step)

All sentences from a recipe are assigned with a sentence identifier. A sentence ID is formatted as "<recipe_id>::<step_id>::<sent_id>" with 1-based indices. All recipes come with a list of ingredients at the beginning. The list is always assigned a step ID "ingredients", and sentences in the ingredients list are not annotated. 


== Annotation columns
Sentences consist of one or more word lines, and word lines contain the following comma separated fields:

ID: Word index, integer starting at 1 for each new sentence; .
FORM: Word form or punctuation symbol.
LEMMA: Lemma of word form.
UPOS: Universal POS tag.
ENTITY: Cooking entities of types: EVENT, HABITAT, TOOL, EXPLICITINGREDIENT and IMPLICITINGREDIENT.
PART: Word index of the head of EVENT entity when the participant-of relation exists between the event and another entity in current line.
RES: Word index of the head of EVENT entity when the result-of relation exists between the event and another entity in current line.
HIDDEN: Hidden entities that are involved in the event in current line; see below for details.
COREF: Coreference ID for entities that are cross-referred. It is represented as LEMMA.step_id.sent_id.token.id, e.g. asparagus.2.1.3.
PREDICATE: The sense of the word that is annotated as a predicate.
ARG1: The arguments of the first predicate in current sentence.
12-15. ARGX: The arguments of the X-th predicate in current sentence.

== Cooking Role Labeling (CRL) annotations

CRL is a domain-specific dependency relation annotation for the cooking domain. Each entity is assigned with a entity ID in addition to the token ID. The entity IDs are in the COREF column of the first token of entities. 

=== Cooking entities
EXPLICITINGREDIENT - listed in the ingredients section of the recipe
IMPLICITINGREDIENT - intermediate outputs of applying a cooking action to a set of explicit ingredients
TOOL - tools that are implicated in the creation of the dish (e.g. spoon, knife, etc.)
HABITAT - habitats that are implicated in the creation of the dish (e.g. oven, bowl, etc.)

=== Cooking Role values in the dependency: participant / result 
participant-of (PART) - this is meant to identify relationships between the event and another cooking entity in the same sentence where the cooking entity is involved in the event. The type of the cooking entity could be HABITAT, TOOL, EXPLICITINGREDIENT or IMPLICITINGREDIENT.
result-of (RES) - this is meant to identify relationships between the event and another entity of type EXPLICITINGREDIENT or IMPLICITINGREDIENT in the same sentence (result link cannot be a hidden relation, see below for description of hidden arguments). In the sentence, "Shape with hands into a ball" the ball is the result of the shape action, which took place on a dropped plum (from an earlier sentence). 

=== hidden roles
These can only appear in the same row where the token is the head of the EVENT entity. Each hidden argument writes as Keyword=value, e.g. Drop=mixture, with multiple values separated by : (e.g. Drop=mixture:olive oil) and multiple hidden attributes separated by | (e.g. Drop=mixture:olive oil|Tool=spoon)

Syntactically elided (DROP) - this occurs when an argument is not mentioned in a sentence but is expected by the verb’s subcategorization. For example, 
"Chop onions." "Simmer [DROP=onions] until browned." The DROP argument is the missing Direct Object of the verb simmer. 
Semantically elided (SHADOW) - this expresses a link between events and semantically hidden ingredients. "Cook pasta in a large pot" necessitates water in the pot, which may have been added previously as a hidden argument (see below for description of hidden arguments).
TOOL - this links objects with the events they are used in. Tools may appear in the text ("Cut the pear with a sharp knife"), or they may be hidden ("Cut an apple" requires an unmentioned knife). 
HABITAT - this links events with the objects in which they take place. Habitats may appear in the text ("Bake in a preheated oven"), or they may be hidden ("Saute the onion" requires an unmentioned pan). 
RESULT - this links events with the objects in which they are a result of. "mixture" is a hidden RESULT of "mix all the ingredients together in the blender".

=== coreference
A coreference id is represented as step_id.sent_id.token_id of the first appearance of the co-referral, e.g. Drop=mixture:olive oil.1.1.3|Tool=spoon (the head of the first appearance of olive oil is the 3rd token of step 1, sentence 1)

== Semantic Role Labeling (SRL) annotations
One of the three layers with which steps in R2VQ are annotated is the Semantic Role Labeling (SRL) layer. SRL is often described informally as the task of automatically answering the question "Who did What to Whom, Where, When, and How?" (Marquéz et al., 2008). More precisely, SRL is usually defined as the task of automatically identifying and labeling argument structures.

Let’s consider the example "John loves Mary". In this case, SRL consists of i) identifying "loves" as a predicate, that is, something that denotes an action or an event; ii) disambiguating the predicate, that is, assigning the most appropriate sense for "loves" in this context; iii) identifying the arguments of each predicate, that is, those parts of the text, "John" and "Mary" that are semantically linked to "loves"; and iv) assigning a semantic role to each predicate-argument pair, e.g., "John" is the Experiencer of the predicate "loves", whereas "Mary" is the Stimulus.

In the context of our evaluation exercise, we employ SRL in its span-based approach, hence tagging the whole span of arguments in given sentences and not just their syntactic heads (e.g., "the broccoli" and not "the"). We chose VerbAtlas (Di Fabio et al., 2019 - http://verbatlas.org/) as our reference inventory of frames and semantic roles and initially labeled the recipes from the dataset automatically, by means of a state-of-the-art system (Conia and Navigli, 2020). Subsequently, we asked human annotators to validate and correct both frames and argument labels to ensure data quality.

Predicate frames: each predicate is labeled according to its VerbAtlas sense/frame in column 10 of the file. A value of ‘_’ means that the corresponding word is not a predicate. In the example below, there is only one predicate, "Cut" with the corresponding sense/frame "CUT" in position 1.

SRL example (omitted some columns for readability):
1 Cut           [...]    CUT    B-V
2 the           [...]    _      B-Patient
3 broccoli      [...]    _      I-Patient
4 into          [...]    _      B-Result
5 flowerets     [...]    _      I-Result 
6 .             [...]    _      _

Semantic roles: for each predicate, we provide its semantic roles in BIO format (B - Beginning, I - Inside, O - Outside). Note that, for this dataset, we only use B and I to indicate the first token of a span and the rest of the tokens in the same span, respectively. In the example above, "the broccoli" is a Patient of the predicate CUT, with the token "the" as the Beginning of the span (B-Patient) and the token "broccoli" as the Inside of the span (I-Patient). 
Note that the predicate that refers to a specific column of semantic roles is always labeled with the notation B-V. Should the predicate consist of a multi-word expression, the other tokens apart from the first are labeled as I-V:

1 Deep   [...]    COOK    B-V
2 -      [...]    _       I-V
3 fry    [...]    _       I-V
4 till   [...]    _       B-Result
5 crispy [...]    _       I-Result
6 &      [...]    _       I-Result
7 golden [...]    _       I-Result
8 brown  [...]    _       I-Result

Should the multi-word expression be made of non-adjacent words, tokens apart from the first are instead labeled as D-V: 

1 Bring   [...]    CHANGE_APPEARANCE/STATE    B-V
2 the     [...]    _                          B-Patient
3 water   [...]    _                          I-Patient
4 to      [...]    _                          D-V
5 boil    [...]    _                          D-V 
6 .       [...]    _                          _

In the case of multiple predicates in the same sentence, there will be multiple semantic role columns, one for each predicate in column 10. For example, if there are two predicates in the sentence, column 11 will indicate the semantic roles for the first predicate, and column 12 will show the semantic roles for the second predicate. 

1 Reduce   [...]    REDUCE_DIMINISH     B-V          _
2 heat     [...]    _                   B-Attribute  _
3 ,        [...]    _                   _            _
4 and      [...]    _                   _            _
5 simmer   [...]    COOK                _            B-V
6 for      [...]    _                   _            B-Time
7 1        [...]    _                   _            I-Time
8 hour     [...]    _                   _            I-Time
9 .        [...]    _                   _            _

== Image annotation

Accompanying each recipe is a series of images extracted from YouTube videos that are associated with a particular event in the recipe. The images were pulled from a set of YouTube videos that were selected by querying YouTube for recipe titles and for the text of each event. For each query, Creative Commons licensed videos were downloaded. These videos were indexed by generating an embedding using the tensorflow implementation of the S3D model available [here](https://tfhub.dev/deepmind/mil-nce/s3d/1). For each event in the recipes, the closest 5 video clips were selected. Annotators then reviewed the retrieved clips and excluded any poor matches. Events with no matching images in the first 5 results currently have no images in the dataset. More images will be added in the coming weeks. Images are stored in directories with names that correspond to the step in the recipe. For example, the images stored in the directory /data/f-2J5PPZWS/f-2J5PPZWS_step02_sent01_000 were aligned to step 2, sentence 1, token 0 of the recipe with ID f-2J5PPZWS.

=================================================================================
LICENSE
=================================================================================

The data is released under the CC-BY-NC 4.0 license (see LICENSE.txt). If you use
the data, please cite the paper below.


=================================================================================
REFERENCE
=================================================================================

Plain text:
James Pustejovsky, Jingxuan Tu, Marco Maru, Simone Conia, Roberto Navigli, Kyeongmin Rim, Kelley Lynch, Richard Brutti, Eben Holderness. SemEval-2022 Task 9: R2VQ - Competence-based Multimodal Question Answering. In Proceedings of the 16th Workshop on Semantic Evaluation (SemEval-2022).

BibTex:
@inproceedings{pasini-etal-xl-wsd-2021,
    title={{SemEval-2022} {T}ask 9: {R2VQ} - Competence-based Multimodal Question Answering},
    author={Pusejovsky, James and Tu, Jingxuan and Maru, Marco and Conia, Simone and Navigli, Roberto and Rim, Kyeongmin and Lynch, Kelley and Brutti, Richard and Holderness, Eben},
    booktitle={Proceedings of the 16th Workshop on Semantic Evaluation (SemEval-2022)},
    year={2022}
}


=================================================================================
CONTACTS
=================================================================================

James Pustejovsky, Brandeis University, jamesp@brandeis.edu
Jingxuan Tu, Brandeis University, jxtu@brandeis.edu
Marco Maru, Sapienza University of Rome, maru@di.uniroma1.it
Simone Conia, Sapienza University of Rome, conia@di.uniroma1.it
Roberto Navigli, Sapienza University of Rome, navigli@diag.uniroma1.it
Kyeongmin Rim, Brandeis University, krim@brandeis.edu
Kelley Lynch, Brandeis University, kmlynch@brandeis.edu
Richard Brutti, Brandeis University, richardbrutti@brandeis.edu
Eben Holderness, Brandeis University, egh@brandeis.edu


