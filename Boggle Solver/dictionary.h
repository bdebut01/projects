#ifndef	DICT_H
#define	DICT_H

/*
 * Dictionary interface
 *     purpose: store words
 *   functions: see public functions
 *        uses: Node class to build the trie
 */

#include	<iostream>
using namespace std;

#define	N_LETTS	26

class Node
{
	public:
		Node();					// constructor
		Node* get_link(int pos);		// get link for pos 
		bool  set_link(int pos,Node* p);	// set link for pos
		bool  get_is_word();			// is node endOfWord?
		void  set_is_word(bool);		// set endOfWord val
	private:
		Node *links[N_LETTS];
		bool is_word;
};
		
class Dictionary
{
	public:
		Dictionary();			// create/init one
		~Dictionary();			// create/init one
		bool insert(string);		// rets: false if fails
		bool isPrefix(string);		// 
		bool isWord(string);

	private:
		Node *root;
};

#endif
