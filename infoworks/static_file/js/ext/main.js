
function default_main_store(){
	Ext.define('Data', {
	    extend: 'Ext.data.Model',
	    fields: [
	       {name: 'id', type: 'string'},
	       {name: 'school_indicator_dataset__school_year__school_year', type: 'string'},
	       {name: 'dimension_x', type: 'string'},
	       {name: 'dimension_y', type: 'string'},
	       {name: 'key_value',  type: 'string'},
	       {name: 'data_type', type: 'string'}
	    ],
	    idProperty: 'data'
	});
	
	var store = Ext.create('Ext.data.ArrayStore', {
	        model: 'Data',
	        data: []
	});
    return store;
}

function default_main_column(){
    return [
            {text : 'Dimension Y', width : "38%", sortable : true, dataIndex: 'dimension_y'},
            {text : 'Dimension X', width : "15%", sortable : true, dataIndex: 'dimension_x'},
            {text : 'School Year', width : "15%", sortable : true, dataIndex: 'school_indicator_dataset__school_year__school_year'},
            {text : 'Data Type', width : "15%", sortable : true, dataIndex: 'data_type'},
            {text : 'Value', width : "15%", sortable : true, dataIndex: 'key_value'}
        ];
}


main =  {title: 'Table',
        xtype: 'grid',
        collapsible: false,
        scrollable: true,
        region: 'center',
        margin: '5 0 0 0',
        store: default_main_store(),
        stateful: true,
        collapsible: true,
        multiSelect: true,
        scrollable: true,
        layout: 'fit',
        id: 'main',
        selType: 'checkboxmodel',
        columns: default_main_column(),
        plugins :[{ ptype :'exportrecords',  downloadButton  : 'top' }],
        viewConfig: {
            stripeRows: true,
            enableTextSelection: true,
            forceFit: true,
        },
        dockedItems: [{
            xtype: 'toolbar',
            dock: 'bottom',
            ui: 'footer',
            layout: {
                pack: 'center'
            },
            items: [{
                id:"compare_school_year",
                text: 'Compare with school year',
                disabled: true,
                listeners:{
                    click: function(){
                        main_table = Ext.getCmp("main").getSelectionModel();
                        items = main_table.selected.items;
                        console.log(items);
                        l = [];
                        for (var i = 0; i < items.length; i++){
                        	l.push(items[i].data.id);
                        }
                        table = Ext.getCmp("main");
                        param = l.toString();
                        Ext.getCmp('compare_school_year').disable();
                        Ext.getCmp('compare_school').disable();
                        Ext.Ajax.request({
                            url: "/api/school_tabledata",
                            timeout: 60000,
                            method: 'GET',
                            scope: this,
                            disableCaching:false,
                            params: "compare=school_year&indicatordata_ids="+param,
                            success: function(resp) {

                               data = JSON.parse(resp.responseText)
                               console.log(data);
                               Ext.define('Data', {
								    extend: 'Ext.data.Model',
								    fields: data.fields,
								    idProperty: 'data'
								});
								
								var new_store = Ext.create('Ext.data.ArrayStore', {
								        model: 'Data',
								        data: data.data
								});
                                
								categories = cover_categories(data.columns);
								series = cover_series(data.data);
								chart = new InforChart (categories, series);
								chart.showChart();
								table.reconfigure(new_store, data.columns);
                               
                            }
                         });
                        table.getSelectionModel().deselectAll();
                         
                    }
                }
            },{
                id: 'compare_school',
                text: 'Compare with school',
                disabled: true,
                listeners:{
                    click: function(){
                        main_table = Ext.getCmp("main").getSelectionModel();
                        items = main_table.selected.items;
                        console.log(items);
                        l = [];
                        for (var i = 0; i < items.length; i++){
                        	l.push(items[i].data.id);
                        }
                        table = Ext.getCmp("main");
                        param = l.toString();
                        Ext.getCmp('compare_school_year').disable();
                        Ext.getCmp('compare_school').disable();
                        Ext.Ajax.request({
                            url: "/api/school_tabledata",
                            timeout: 60000,
                            method: 'GET',
                            scope: this,
                            disableCaching:false,
                            params: "compare=school&indicatordata_ids="+param,
                            success: function(resp) {
                               
                               data = JSON.parse(resp.responseText)
                               console.log(data);
                               Ext.define('Data', {
								    extend: 'Ext.data.Model',
								    fields: data.fields,
								    idProperty: 'data'
								});
								
								var new_store = Ext.create('Ext.data.ArrayStore', {
								        model: 'Data',
								        data: data.data
								});
                               
								categories = cover_categories(data.columns);
								series = cover_series(data.data);
								chart = new InforChart (categories, series);
								chart.showChart();
                                table.reconfigure(new_store, data.columns);
                            }
                         });
                        table.getSelectionModel().deselectAll();
                         
                    }
                }
            }]
        }]
    };

//Create the Download button and add it to the top toolbar

