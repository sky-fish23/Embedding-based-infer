import openke
from openke.config import Trainer, Tester
from openke.module.model import TransD
from openke.module.loss import MarginLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader

# import time
# start = time.time()

# dataloader for training
train_dataloader = TrainDataLoader(
	in_path = "./datasetProcess/newData/AUTO/", 
	nbatches = 100,
	threads = 8, 
	sampling_mode = "normal", 
	bern_flag = 1, 
	filter_flag = 1, 
	neg_ent = 25,
	neg_rel = 0)

# dataloader for test
test_dataloader = TestDataLoader("./datasetProcess/newData/AUTO/", "link")

# define the model

transd = TransD(
	ent_tot = train_dataloader.get_ent_tot(),
	rel_tot = train_dataloader.get_rel_tot(),
	dim_e = 200, 
	dim_r = 200, 
	p_norm = 1, 
	norm_flag = True)


# define the loss function
model = NegativeSampling(
	model = transd, 
	loss = MarginLoss(margin = 5.0),
	batch_size = train_dataloader.get_batch_size()
)


# train the model
trainer = Trainer(model = model, data_loader = train_dataloader, train_times = 1000, alpha = 1.0, use_gpu = True)
trainer.run()
transd.save_checkpoint('./checkpoint/transd_AUTO.ckpt')

transd.save_parameters('./embed/transd_AUTO_embed.vec') # 保存嵌入向量

# test the model
transd.load_checkpoint('./checkpoint/transd_AUTO.ckpt')
tester = Tester(model = transd, data_loader = test_dataloader, use_gpu = True)
tester.run_link_prediction(type_constrain = False)

# end = time.time()
# print(end - start)