# from ogb.graphproppred import Evaluator
# import torch
# from ogb.graphproppred.mol_encoder import AtomEncoder, BondEncoder
#
# import hydra
# import torch
# from omegaconf import DictConfig
# from pytorch_lightning import LightningModule
# from pytorch_lightning.metrics.classification import Accuracy
#
#
# class OGBGPpaModel(LightningModule):
# def __init__(self, architecture: DictConfig, optimizer: DictConfig):
#     super().__init__()
#         self.save_hyperparameters()
#         self.atom_encoder = AtomEncoder(emb_dim=self.hparams.node_emb_size)
#         # self.bond_encoder = BondEncoder(emb_dim=self.hparams.edge_emb_size)
#
#         if self.hparams.architecture == "GCN":
#             self.architecture = GCN(hparams=self.hparams)
#         elif self.hparams.architecture == "GAT":
#             self.architecture = GAT(hparams=self.hparams)
#         elif self.hparams.architecture == "GraphSAGE":
#             self.architecture = None
#         else:
#             raise Exception("Invalid architecture name")
#
#         self.criterion = torch.nn.CrossEntropyLoss()
#
#         self.evaluator = Evaluator(name="ogbg-ppa")
#         self.train_acc_hist = []
#         self.val_acc_hist = []
#
#     def forward(self, batch):
#         batch.x = self.atom_encoder(batch.x)
#         # batch.edge_attr = self.bond_encoder(batch.edge_attr)
#         return self.architecture(batch)
#
#     # logic for a single training step
#     def training_step(self, batch, batch_idx):
#         y_pred = self.forward(batch)
#         loss = self.criterion(y_pred, batch.y.to(torch.float32))
#         y_true = batch.y.view(y_pred.shape)
#
#         # training metrics
#         self.log('train_loss', loss, on_step=False, on_epoch=True, prog_bar=False)
#
#         return {"loss": loss, "y_pred": y_pred, "y_true": y_true}
#
#     # logic for a single validation step
#     def validation_step(self, batch, batch_idx):
#         y_pred = self.forward(batch)
#         loss = self.criterion(y_pred, batch.y.to(torch.float32))
#         y_true = batch.y.view(y_pred.shape)
#
#         # training metrics
#         self.log('val_loss', loss, on_step=False, on_epoch=True, prog_bar=False)
#
#         return {"loss": loss, "y_pred": y_pred, "y_true": y_true}
#
#     # logic for a single test step
#     def test_step(self, batch, batch_idx):
#         y_pred = self.forward(batch)
#         loss = self.criterion(y_pred, batch.y.to(torch.float32))
#         y_true = batch.y.view(y_pred.shape)
#
#         # training metrics
#         self.log('test_loss', loss, on_step=False, on_epoch=True, prog_bar=False)
#
#         return {"loss": loss, "y_pred": y_pred, "y_true": y_true}
#
#     def configure_optimizers(self):
#         if self.hparams.optimizer == "adam":
#             return torch.optim.Adam(self.parameters(), lr=self.hparams.lr, weight_decay=self.hparams.weight_decay)
#         else:
#             raise Exception("Invalid optimizer name")
#
#     def training_epoch_end(self, outputs):
#         acc = self.calculate_metric(outputs)
#         self.train_acc_hist.append(acc)
#         self.log("train_acc", acc, prog_bar=True)
#         self.log("train_acc_best", max(self.train_acc_hist), prog_bar=True)
#
#     def validation_epoch_end(self, outputs):
#         acc = self.calculate_metric(outputs)
#         self.val_acc_hist.append(acc)
#         self.log("val_acc", acc, prog_bar=True)
#         self.log("val_acc_best", max(self.val_acc_hist), prog_bar=True)
#
#     def test_epoch_end(self, outputs):
#         self.log("test_acc", self.calculate_metric(outputs), prog_bar=False)
#
#     def calculate_metric(self, outputs):
#         y_true = torch.cat([x["y_true"] for x in outputs], dim=0)
#         y_pred = torch.cat([x["y_pred"] for x in outputs], dim=0)
#         result_dict = self.evaluator.eval({"y_true": y_true, "y_pred": y_pred})
#         return result_dict["acc"]
