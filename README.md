# FutureYou NLP Search Engine

Approach: Python3 with NLTK's wordnet.
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



By specifying a wordnet ID to wordnet, one can obtain the appropriate synonyms, hypernyms and hyponyms of the words.
  1. Synonyms: words with similar meanings as a word
      Word: accounting.n.04
      Synonyms:-
      accounting
      accounting_system
      method_of_accounting
  2. Hypernyms: words that superset a word
      Word: accountant.n.01<br /> - someone who maintains and audits business accounts
      Hypernyms:-
      businessperson.n.01, definition: a capitalist who engages in industrial commercial enterprise
  3. Hyponyms: words that is a subclass of a word
      Word: accountant.n.01, Definition: someone who maintains and audits business accounts
      Hyponyms:-
      auditor.n.03, definition: a qualified accountant who inspects the accounting records and practices of a business or other organization
      bean_counter.n.01, definition: an accountant or bureaucrat who is believed to place undue emphasis on the control of expenditures
      bookkeeper.n.01, definition: someone who records the transactions of a business
      certified_public_accountant.n.01, definition: an accountant who has passed certain examinations and met all other statutory and licensing requirements of a United States state to be certified by that state
      chartered_accountant.n.01, definition: a British or Canadian accountant who is a member of a professional body that has a royal charter
      cost_accountant.n.01, definition: a specialist in the systematic recording and analysis of the costs incident to production

What I did:
  1. For each of the careers (200-ish in total), David and I specified some words that are related to it.
  2. For each of the words we used, I specified the appropriate context in wordnet
  3. I make a dictionary, mapping the interests to a list of related careers.
  4. I wrote a server app, that takes in a list of terms. (NOTE: can only handle single words at the moment)
    a. First, I find the wordnet synsets (wordnet object that holds the contextIds of a word) for the search terms.
    b. I then perform a breadth-first search in wordnet, exploring its synonyms, hypernyms and hyponyms (up to a depth of 2).
    c. If one of the wordnet synsets explored is part of the defined interest contexts (in 2),
        I add the careers it maps to into the response JSON

Advantages:
  1. Can return results when using forms of words, such as "construction", "constructing", "construct".
  2. Handles synonyms decently without the use of external APIs.

Disadvantages:
  1. Results do not always include careers we expect. E.g. "Mental" does not return "Psychologist"
      More work required to improve it
  2. Requires manual input of related words, and specification of context
