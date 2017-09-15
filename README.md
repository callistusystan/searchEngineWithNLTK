# Search Engine with Wordnet

## Approach: Python3 with NLTK's <strong>Wordnet</strong>.

#### What is Wordnet?
Wordnet is a library that contains all the English words, as well as their contexts. Words are connected to one another in a graph-like manner.

Below is an example of all the contexts for the word "accounting" in wordnet,
<ol>
  <li>
  wordnet ID: accounting.n.01<br /> - a convincing explanation that reveals basic causes
  </li>
  <li>
  wordnet ID: accounting.n.02<br /> - a system that provides quantitative information about finances
  </li>
  <li>
  wordnet ID: accountancy.n.01<br /> - the occupation of maintaining and auditing records and preparing financial reports for a business
  </li>
  <li>
  wordnet ID: accounting.n.04<br /> - a bookkeeper's chronological list of related debits and credits of a business; forms part of a ledger of accounts
  </li>
  <li>
  wordnet ID: account.n.07<br /> - a statement of recent transactions and the resulting balance
  </li>
  <li>
  wordnet ID: account.v.01<br /> - be the sole or primary factor in the existence, acquisition, supply, or disposal of something
  </li>
  <li>
  wordnet ID: account.v.02<br /> - keep an account of
  </li>
  <li>
  wordnet ID: report.v.01<br /> - to give an account or representation of in words
  </li>
  <li>
  wordnet ID: account.v.04<br /> - furnish a justifying analysis or explanation
  </li>
</ol>

By specifying a wordnet ID to wordnet, one can obtain the appropriate synonyms (similar words), hypernyms (categories a word belongs to) and hyponyms (words that fit this category) of the words.
<ol>
<li>Synonyms of accounting.n.04:-
<ul>
<li>
accounting
</li>
<li>
accounting_system
</li>
<li>
method_of_accounting
</li>
</ul>
</li>
<li>
Hypernyms of accountant.n.01:-
<ul>
businessperson.n.01
</ul>
</li>
<li>
Hyponyms of accountant.n.01:-
<ul>
<li>
auditor.n.03
</li>
<li>
bean_counter.n.01
</li>
<li>
bookkeeper.n.01
</li>
<li>
certified_public_accountant.n.01
</li>
<li>
chartered_accountant.n.01
</li>
<li>
cost_accountant.n.01
</li>
</li>
</ol>

#### What I did:
<ol>
<li>
  For each of the careers (200-ish in total), David and I specified some words that are related to it.
  </li>
  <li>
  For each of the words we used, I specified the appropriate context in wordnet
  </li>
  <li>
  I then create a dictionary, mapping the interests to a list of related careers.
  </li>
  <li>
  I wrote a server app, taking in a list of terms. (NOTE: can only handle single words at the moment)
  <ul>
    <li>
    First, I find the wordnet synsets (wordnet object that holds the contextIds of a word) for the search terms.
    </li>
    <li>
    I then perform a breadth-first search in wordnet, exploring its synonyms, hypernyms and hyponyms (up to a depth of 2).
    </li>
    <li>
    If one of the wordnet synsets explored is part of the defined interest contexts (in 2),
        I add the careers it maps to into the response JSON
    </li>
  </ul>
  </li>
</ol>

#### Advantages:
  1. Handles synonyms decently without the use of external APIs.
  2. Can return results when using forms of words, such as "construction", "constructing", "construct" and find matches.

#### Disadvantages:
  1. Requires manual input of related words, and specification of context
  2. Results do not always include careers we expect. E.g. "Mental" does not return "Psychologist"

## Screenshots
<div>
<img src="/screenshots/screenshot1.png" width="480">
<img src="/screenshots/screenshot2.png" width="480">
</div>
