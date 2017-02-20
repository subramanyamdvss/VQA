from vqaTools.vqa import VQA
import random
import skimage.io as io
import matplotlib.pyplot as plt
import os
import collections

dataDir='/users/Datasets/VQA/data'
taskType='OpenEnded'
dataType='mscoco' # 'mscoco' for real and 'abstract_v002' for abstract
dataSubType='train2014'
annFile='%s/Annotations/%s_%s_annotations.json'%(dataDir, dataType, dataSubType)
quesFile='%s/Questions/%s_%s_%s_questions.json'%(dataDir, taskType, dataType, dataSubType)
imgDir = '%s/%s/' %(dataDir, dataSubType)


class preprocessing:
	def __init__(self, annotation_file=annFile, question_file=quesFile):
		self.vqar=VQA(annFile, quesFile)
		self.annIds = self.vqar.getQuesIds()
		self.anns = self.vqar.loadQA(self.annIds)  #every questions with the dictionary loaded

		self.l=[a['multiple_choice_answer'] for a in self.anns]
		self.c=collections.Counter(self.l)
		self.Selected_key=[]
		self.Selected_keys={}
		self.i=0
		for a in self.c.most_common(1000):
			self.Selected_key.extend([a[0]])
			self.Selected_keys[a[0]] = self.i
			self.i+=1

		self.Question_element=[]
		for ele in self.anns:
			if ele['multiple_choice_answer'] in self.Selected_keys.keys():
				self.Question_element.extend([ele])
		self.qqa = {}
		self.qqa = {ann['question_id']:       [] for ann in self.Question_element}
		print 'assigning questions '
		y=0
		for ques in self.vqar.questions['questions']:
			print 'done',y
			y+=1
			if ques['question_id'] in self.qqa.keys():
				self.qqa[ques['question_id']] = ques
		print 'assigning questions finished'
		ques_words=[]
		for ann in self.Question_element:
			quesId = ann['question_id']
			for words in self.qqa[quesId]['question']:
				ques_words.extend([words])
		s=collections.Counter(ques_words)
		self.Selected_ques={}
		j=0
		for a in s.most_common(5000):
			self.Selected_ques[a[0]] = j
			j+=1

		print 'elements list completed'

	def load_class_dict(self):
		return self.Selected_keys

	def load_Q_final(self):
		return self.Selected_ques
