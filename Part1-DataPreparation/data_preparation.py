#!/usr/bin/env python
import torch
from torch.utils				import Dataset
from sklearn.utils			import shuffle
from ROOT								import TFile
from Scripts.DataFormat import Particle
from Scripts.DataFormat import get_leptons, get_prompt_leptons, get_jets

def preselect(evt, muons, electrons, jets):
    ### Preselection ###
    # 1. 1e2mu
    # 2. should pass triggers and safe cuts
    # 3. Nj >= 2
    if not (len(muons) == 2 and len(electrons) == 1):
        return False
    if not (evt.passDblMuTrigs or evt.passEMuTrigs):
        return False
    pass_safecut = ((muons[0].Pt() > 20. and muons[1].Pt() > 10.) or
                    (muons[0].Pt() > 25. and electrons[0].Pt() > 15.) or
                    (muons[0].Pt() > 10. and electrons[0].Pt() > 25.))
    if not pass_safecut:
        return False
    return True


def rtfile_to_datalist(rtfile, is_signal, max_len=15000):
		### Convert rtfile events to torch tensor objects
		datalist = []
		for evt in rtfile.Events:
				muons, electrons = get_leptons(evt)
				jets, bjets = get_jets(evt)
				METv = Particle(evt.METv_pt, 0., evt.METv_phi, 0.)

				# events should pass preselection
				if not preselect(evt, muons, electrons, jets):
						continue

				muons_prompt, electrons_prompt = get_prompt_leptons(muons, electrons)
				is_prompt_evt = (len(muons) == len(muons_prompt) and len(electrons) == len(electrons_prompt))
				if not is_signal and not is_prompt_evt:	pass		# fake events
				elif is_signal and is_prompt_evt: pass					# signal events
				else: continue

				### store muon and electron information
				features = []
				for lepton in muons+electrons:
						features.append(lepton.Pt())
						features.append(lepton.Eta())
						features.append(lepton.Phi())
						features.append(lepton.M())
						features.append(lepton.Charge())
						features.append(lepton.IsMuon())
						features.append(lepton.IsElectron())
				for jet in jets[:2]:
						features.append(jet.Pt())
						features.append(jet.Eta())
						features.append(jet.Phi())
						features.append(jet.M())
						features.append(jet.BtagScore())
				datalist.append((torch.tensor(features, dtype=torch.float), torch.tensor(is_signal, dtype=torch.long)))

				if len(datalist) == max_len: break

		try:
				assert len(datalist) == max_len
				print(f"{max_len} events has been converted to torch tensor format")
		except:
				print(f"not enough events to convert, rtfile has {len(datalist)} events!")
				pass

		return datalist


class MyDataset(Dataset):
		def __init__(self, datalist):
				super(MyDataset, self).__init__()
				self.datalist = datalist

		def __len__(self):
				return len(self.datalist)

		def __getitem__(self, idx):
				return self.datalist[idx]


if __name__ == "__main__":
		f_sig = TFile.Open("SelectorOutput/2017/Skim1E2Mu__/Selector_TTToHcToWA_AToMuMu_MHc130_MA90.root")
		f_bkg = TFile.Open("SelectorOutput/2017/Skim1E2Mu__/Selector_TTLL_powheg.root")

		datalist = rtfile_to_datalist(f_sig, is_signal=True, max_len=16) + rtfile_to_datalist(f_bkg, is_signal=False, max_len=16)
		datalist = shuffle(datalist, random_state=304)
		dataset = MyDataset(datalist)
		print(len(dataset))
		print(dataset[0])
		print(dataset[1])
		print(dataset[2])
