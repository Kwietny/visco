## Resources
- [RDKit](https://www.rdkit.org/)
- [Scikit-fingerprints](https://scikit-fingerprints.readthedocs.io/stable/)

## Current results
AUC

| classifier\features                 | expert_chen(surf) | expert_chen(all) | physiochemical(surf) | physiochemical(all) |
|-------------------------------------|-------------------|------------------|----------------------|---------------------|
| RandomForest(n=10, leaf=10)         | 0.8224 ± 0.0053   | 0.8330 ± 0.0069  | 0.8102 ± 0.0043      |                     |
| HistGradientBoosting(i=200, lr=0.1) | 0.8382 ± 0.0074   | 0.8542 ± 0.0094  | 0.8631 ± 0.0096      | super slow          |
| XGBoost(n=300, d=5, lr=0.05)        | 0.8460 ± 0.0056   | 0.8647 ± 0.0072  | 0.8667 ± 0.0082      | 0.8580 ± 0.0064     |

### Relevant feature ideas
- chain length(maybe just no. of carbon atoms?)
- no. of tails
- tail structure(how to encode meaningfully?)
- headgroup type(anionic etc.)
- headgroup charge/size/hydrogen bonding

### Descriptors idea (from the paper)
* Expert
  * Surfactant: 
  * molecular weight
  * surfactant type - anionic, cationic, zwitterionic, nonionic
  (potentially more advanced from [Surfactants-PUT](https://github.com/ashansaleha-collab/Surfactants-PUT/blob/main/cli/features/expert.py))
  * carbon tail length (leading Cs)
  * Additive???
* Chen

```Python
from rdkit import Chem
from rdkit.Chem import QED, Descriptors, EState, GraphDescriptors, MolSurf

mol = Chem.MolFromSmiles(smiles)

descriptors = {
    "index": idx,
    "chen_MolLogP": Descriptors.MolLogP(mol),
    "chen_Chi1v": GraphDescriptors.Chi1v(mol),
    "chen_VSA_EState7": EState.EState_VSA.EState_VSA7(mol),
    "chen_VSA_EState8": EState.EState_VSA.EState_VSA8(mol),
    "chen_qed": QED.qed(mol),
    "chen_FpDensityMorgan1": Descriptors.FpDensityMorgan1(mol),
    "chen_SMR_VSA5": MolSurf.SMR_VSA5(mol),
    "chen_PEOE_VSA6": MolSurf.PEOE_VSA6(mol),
    "chen_MinPartialCharge": Descriptors.MinPartialCharge(mol),
    "chen_BertzCT": GraphDescriptors.BertzCT(mol),
    "chen_VSA_EState1": EState.EState_VSA.EState_VSA1(mol),
    "chen_MaxAbsEStateIndex": EState.MaxAbsEStateIndex(mol),
    "chen_Balaban": GraphDescriptors.BalabanJ(mol),
    "chen_SlogP_VSA2": MolSurf.SlogP_VSA2(mol),
    "chen_HallKierAlpha": Descriptors.HallKierAlpha(mol),
    "chen_EState_VSA5": EState.EState_VSA.EState_VSA5(mol),
    "chen_MaxPartialCharge": Descriptors.MaxPartialCharge(mol),
    "chen_PEOE_VSA7": MolSurf.PEOE_VSA7(mol),
    "chen_PEOE_VSA8": MolSurf.PEOE_VSA8(mol),
}
```  
* Physiochemical feature set from [sklearn-firngerprints](https://scikit-fingerprints.readthedocs.io/stable/modules/generated/skfp.fingerprints.PhysiochemicalPropertiesFingerprint.html)
```Python
import skfp.fingerprints as sfp

features = sfp.PhysiochemicalPropertiesFingerprint(fp_size=256)
```

#### Notes  
- using Critical Micelle Concentration may be useful for prediction 
- do we have access just to measurement at this one frequency(what even is the frequency at G''min) or to entire spectrum data?
- how to classify additives/what properties to use as features
- check upper and lower surfactant concentration ratio
- check not viscoelastic mixtures which have high eta_0