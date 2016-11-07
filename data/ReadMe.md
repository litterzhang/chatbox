# 问题定义
id : 标识问题  
type : 0 , 1 , 2。 0表示会话确定问题，在一次会话中，答案唯一；1表示会话发散问题，在一次会话中，答案可以有多种；2表示未知问题  
content : 问题内容  
words : 问题分词  

# 答案定义
id : 标识答案  
type : 0 , 1 , 2。 0表示正向回答，1表示负向回答，2表示中立回答。  
seed : 标识回答的中心。  
deg : 标识回答的情绪程度
content : 回答内容  
words ： 回答关键词

# 问题——答案定义
que_id : 问题id
ans_ids : [答案id]