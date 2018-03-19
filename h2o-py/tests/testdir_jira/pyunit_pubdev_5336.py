import h2o
import pandas as pd
import numpy as np
from tests import pyunit_utils


def pubdev_5336():
    data = pd.DataFrame({'Origin': ['SFO', 'SAN', 'SFO', 'NYC', np.nan],
                         'Dest': ['SFO', 'SFO', 'SAN', 'SAN', np.nan]})
    frame = h2o.H2OFrame(data)
    frame['Origin'].asfactor()
    frame['Dest'].asfactor()

    # First column has one more categorical variable
    assert frame['Origin'].nlevels() == [4]
    assert frame['Origin'].levels() == [['NYC', 'SAN', 'SFO', 'nan']];
    assert frame['Dest'].nlevels() == [3]
    assert frame['Dest'].levels() == [['SAN', 'SFO', 'nan']];
    frame['eq'] = frame['Origin'] == frame['Dest']
    assert frame['eq'][0,0] == 1
    assert frame['eq'][1,0] == 0
    assert frame['eq'][2,0] == 0
    assert frame['eq'][3,0] == 0

    # Compare in inverse order (tests one more categorical variable in first column)
    frame['eqInv'] = frame['Dest'] == frame['Origin']
    assert frame['eqInv'][0,0] == 1
    assert frame['eqInv'][1,0] == 0
    assert frame['eqInv'][2,0] == 0
    assert frame['eqInv'][3,0] == 0


    train = h2o.import_file(path=pyunit_utils.locate("smalldata/testng/airlines_train.csv"))
    train['Origin'].asfactor()
    train['Dest'].asfactor()
    train['eq'] = train['Origin'] == train['Dest']
    assert train[train['eq'] == 1].nrows is 0

if __name__ == "__main__":
    pyunit_utils.standalone_test(pubdev_5336)
else:
    pubdev_5336
