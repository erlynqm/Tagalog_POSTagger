##Erlyn Manguilimotan
##Computational Linguistics (NAIST)
import nltk
import re


class tagalogdata():
      def __init__(self, datafile):
          self.datafile =datafile

      def load_data(self): ##load annotated text from file
          annotated_text=[] 
          filename =open(self.datafile)
          data = filename.readlines()
          return data

      def tagged_sentences(self):
          ##transform data into nltk tagged tuples
          data=self.load_data()
          annotated_data=[]
          for sentence in data:
              tagged =[nltk.tag.str2tuple(t) for t in sentence.split()]
              annotated_data.append(tagged)
          return annotated_data

####
class tagalog_stemmer():
    def infix_list(self):
        return {'um', 'in'}

    def prefix_list(self):
        return {'mag', 'nag', 'magsi', 'nagsi', 'mang', 'nang', 'maka', 'naka','magka','magkaka','nagka','nagkaka', 'magma', 'nagma', 'magpa', 'nagpa', 'magpapa', 'nagpapa', 'magpaka', 'nagpaka', 'magpati', 'nagpati', 'mai','ma','na', 'nai', 'maipa', 'naipa', 'maipag', 'naigpag', 'makapag', 'nakapag', 'mapa', 'napa', 'makapang', 'nakapang', 'nakapan', 'makapan', 'makapam', 'nakapam', 'mang', 'nang', 'man', 'nan', 'mam', 'nam', 'mangag', 'nangag', 'i', 'ipa', 'ipaki', 'ipakipa', 'isa', 'ka', 'pa', 'pag', 'papag', 'mapag', 'napag', 'pang', 'ipag', 'ipang', 'pinag', 'ika', 'ikapang', 'paka', 'paki'}
  
    def suffix_list(self):
        return {'an', 'han', 'in', 'hin'}

    def vowel(self): 
        return {'a','e','i','o','u'}

    def strip_infix (self, s):

        prev = '' #previous character
        current = ''  #current character
        position = 0
        cand_infix ='' #candidate infix
        for i in s :
                position +=1 # monitor position. if matched affix is at the end, then it's not infix
                current= prev+i ##combine two characters

                if current.strip() in self.infix_list() and position < (len(s)-1): ##if current combination is in the infix array and not last position
                   cand_infix = current  
			
                prev = i
      
        #print('infix', cand_infix)

        return  re.sub(cand_infix,'',s,1),cand_infix #return the string removing the candidate infix

#################################################

    def prefix_suffix (self,s): ##usually, the prefix appears with a suffix e.g. paghandaan (pag ~~ an)		

        the_suffix=''
        the_prefix=''
        prefix_candidates = []
        suffix_candidates = []
        candidate_root =s.strip()
	
        for pre in sorted(self.prefix_list()):
            if s.startswith(pre):
                   prefix_candidates.append(pre) ##possible to have more than one candidate prefix, e.g.'pa', 'pag'
	
        for suf in self.suffix_list():
            if candidate_root.endswith(suf):
                  suffix_candidates.append(suf) ###find possible candidates "han" "an"

        prev_prefix=''
        prev_root=s
        #print(prefix_candidates)

        for p in prefix_candidates:
                temp1 = re.sub('^'+p,'',s,1) ###remove candidate 
                temp1 = temp1.strip()

                if len(temp1)<4:
                    the_prefix=prev_prefix
                    candidate_root=prev_root
#                    print("temp," ,temp1,the_prefix)
                    break
                else:
                    prev_prefix=p
                    prev_root=temp1

                vowels=self.vowel()
                if temp1[0]  not in vowels and temp1[1] in vowels:
                ## for words that start with consonant or hyphen (mag-ampon, pagkain, paggawa)
                    candidate_root = temp1
                    the_prefix=p
                
        #print("the prefix ", the_prefix)
        if len(candidate_root) > 5:	
               for suf in suffix_candidates:
                   temp1 = re.sub(suf+'$','',candidate_root,1)  ## test to strip out candidate suffix
                   temp1 = temp1.strip()
                   if temp1[len(temp1)-1] is not 'h': ##if word, after removing candidate suffix, does not end with 'h'. tagalog words don't usually end with 'h' 
                            the_suffix = suf
               candidate_root = re.sub(the_suffix+'$','',candidate_root,1)		
               #print('the suffix', the_suffix)

        candidate_root = re.sub('^\W','',candidate_root,1)	### remove hyphen if found (mag-ampon, pag-asa)
        if len(candidate_root) <3 : 
           candidate_root=s

         	
        return candidate_root,the_prefix,the_suffix


    def reduplication(self,word): #reduplication in Tagalog
       redup=''
       if len(word) > 5:  ##for words with length greater than 4. words like 'baba' should not be included
             for i in range(1,3):
                   if word[:i] == word[i:i+i]:  ###python substring; 
                          word= word[i:]
                          redup=(word[:i])
                          break
       return word,redup


    def get_affixes(self,word):
        infix=''
        suffix=''
        prefix=''
        redup=''
        root=''
        temp_word,infix = self.strip_infix(word.lower())	 ###remove any infix first
        temp_word,redup=self.reduplication(temp_word)  ###remove possible reduplication after removing infix ,e.g. kumakain 
        if len(temp_word.strip()) > 4: #usually root words are 4-5 characters in length
               temp_word,prefix,suffix = self.prefix_suffix(temp_word) #try to check prefixes and suffixes
               temp_word,redup=self.reduplication(temp_word) ##remove possible reduplication after removing suffix, e.g. paghahandaan
        root=temp_word

	
        return root.strip(),prefix,infix,suffix,redup


