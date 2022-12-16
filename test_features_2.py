#! using streamlit_aggrid to create a table with drag and drop functionality
# https://discuss.streamlit.io/t/drag-and-drop-rows-in-a-dataframe/33077

 
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import pandas as pd
import numpy as np
import requests



# # OFITIAL EXAMPLE
# import streamlit as st  # pip install streamlit=1.12.0
# import pandas as pd
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, JsCode # pip install streamlit-aggrid==0.2.3

# onRowDragEnd = JsCode("""
# function onRowDragEnd(e) {
#     console.log('onRowDragEnd', e);
# }
# """)

# getRowNodeId = JsCode("""
# function getRowNodeId(data) {
#     return data.id
# }
# """)

# onGridReady = JsCode("""
# function onGridReady() {
#     immutableStore.forEach(
#         function(data, index) {
#             data.id = index;
#             });
#     gridOptions.api.setRowData(immutableStore);
#     }
# """)

# onRowDragMove = JsCode("""
# function onRowDragMove(event) {
#     var movingNode = event.node;
#     var overNode = event.overNode;

#     var rowNeedsToMove = movingNode !== overNode;

#     if (rowNeedsToMove) {
#         var movingData = movingNode.data;
#         var overData = overNode.data;

#         immutableStore = newStore;

#         var fromIndex = immutableStore.indexOf(movingData);
#         var toIndex = immutableStore.indexOf(overData);

#         var newStore = immutableStore.slice();
#         moveInArray(newStore, fromIndex, toIndex);

#         immutableStore = newStore;
#         gridOptions.api.setRowData(newStore);

#         gridOptions.api.clearFocusedCell();
#     }

#     function moveInArray(arr, fromIndex, toIndex) {
#         var element = arr[fromIndex];
#         arr.splice(fromIndex, 1);
#         arr.splice(toIndex, 0, element);
#     }
# }
# """)

# oki = st.file_uploader('Upload your file', type=['csv', 'xlsx'])
# data = pd.read_csv(oki, sep=';', decimal=',', encoding='latin-1').head(10)

# gb = GridOptionsBuilder.from_dataframe(data)
# gb.configure_default_column(rowDrag = False, rowDragManaged = True, rowDragEntireRow = False, rowDragMultiRow=True)
# gb.configure_column('bloco', rowDrag = True, rowDragEntireRow = True)
# gb.configure_grid_options(rowDragManaged = True, onRowDragEnd = onRowDragEnd, deltaRowDataMode = True, getRowNodeId = getRowNodeId, onGridReady = onGridReady, animateRows = True, onRowDragMove = onRowDragMove)
# gridOptions = gb.build()

# data = AgGrid(data,
#             gridOptions=gridOptions,
#             allow_unsafe_jscode=True,
#             update_mode=GridUpdateMode.MANUAL
# )

# st.write(data['data'])



# # EXAMPLE FINAL
import streamlit as st
import pandas as pd
import numpy as np

from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

onRowDragEnd = JsCode("""
function onRowDragEnd(e) {
    console.log('onRowDragEnd', e);
}
""")

getRowNodeId = JsCode("""
function getRowNodeId(data) {
    return data.id
}
""")

onGridReady = JsCode("""
function onGridReady() {
    immutableStore.forEach(
        function(data, index) {
            data.id = index;
            });
    gridOptions.api.setRowData(immutableStore);
    }
""")

onRowDragMove = JsCode("""
function onRowDragMove(event) {
    var movingNode = event.node;
    var overNode = event.overNode;

    var rowNeedsToMove = movingNode !== overNode;

    if (rowNeedsToMove) {
        var movingData = movingNode.data;
        var overData = overNode.data;

        immutableStore = newStore;

        var fromIndex = immutableStore.indexOf(movingData);
        var toIndex = immutableStore.indexOf(overData);

        var newStore = immutableStore.slice();
        moveInArray(newStore, fromIndex, toIndex);

        immutableStore = newStore;
        gridOptions.api.setRowData(newStore);

        gridOptions.api.clearFocusedCell();
    }

    function moveInArray(arr, fromIndex, toIndex) {
        var element = arr[fromIndex];
        arr.splice(fromIndex, 1);
        arr.splice(toIndex, 0, element);
    }
}
""")

df = pd.DataFrame(
    "",
    index=range(10),
    columns=["Bundle"],
)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(rowDrag = False, rowDragManaged = True, rowDragEntireRow = False, rowDragMultiRow=True, editable=True)
gb.configure_column('Bundle',
    cellEditor='agRichSelectCellEditor',
    cellEditorParams={'values':["City tour cusco", "City tour Lima", "Hotel monasterio"]},
    cellEditorPopup=True,
    rowDrag = True,
    rowDragEntireRow = True,
    rowDragManaged = True
)
gb.configure_grid_options(enableRangeSelection=True, rowDragManaged = True, onRowDragEnd = onRowDragEnd, deltaRowDataMode = True, getRowNodeId = getRowNodeId, onGridReady = onGridReady, animateRows = True, onRowDragMove = onRowDragMove)

go =gb.build()

response = AgGrid(
    df,
    gridOptions=go,
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MANUAL,
)

st.write(response['data'])