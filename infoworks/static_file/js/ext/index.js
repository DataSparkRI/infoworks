var chart = new InforChart ([], []);

function clean_school(){
	type = 'school';
    district_code = Ext.getCmp('school_district').value;
    school = Ext.getCmp('school');
    indicator = Ext.getCmp('indicator');
    school_year = Ext.getCmp('school_year');
    school.setValue(null);
    school_type = Ext.getCmp('school_type').value;
    if (school_type==1)
    	school_type='E';
    else if (school_type==2) 
    	school_type='M';
    else if (school_type==3)
        school_type='H';
    else
    	school_type=null;
    if (school_type == null && district_code != null)
        getData("/api/school","district_code="+district_code,school);
    else if (school_type == null && district_code == null)
    	getData("/api/school","",school);
    else if (school_type != null && district_code == null)
    	getData("/api/school","type="+school_type,school);
    else
    	getData("/api/school","type="+school_type+"&district_code="+district_code,school);
    indicator.setValue(null);
    indicator.getStore().loadData([]);
    school_year.setValue(null);
    school_year.getStore().loadData([]);
}

Ext.define('KitchenSink.view.tab.TabController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.tab-view'
});

Ext.define('KitchenSink.view.tab.BasicTabs', {
    extend: 'Ext.tab.Panel',
    xtype: 'basic-tabs',
    controller: 'tab-view',
});


Ext.require([
    'Ext.container.Viewport',
    'Ext.grid.Panel',
    'Ext.grid.plugin.RowEditing',
    'Ext.layout.container.Border'
]);
Ext.Loader.setConfig({
    disableCaching: false
});
Ext.onReady(function() {
	
	Ext.define('Ext.form.field.ComboBoxReset', {
	    extend: 'Ext.form.field.ComboBox',
	    alias: 'widget.comboboxreset',
	    triggers: {
	        clear: {
	            weight: 1,
	            cls: Ext.baseCSSPrefix + 'form-clear-trigger',
	            hidden: true,
	            handler: 'onClearClick',
	            scope: 'this'
	        },
	        picker: {
	            weight: 2,
	            handler: 'onTriggerClick',
	            scope: 'this'
	        }
	    },

	    onClearClick: function () {
	        var me = this;

	        if (me.disabled) {
	            return;
	        }

	        me.clearValue();
	        me.getTrigger('clear').hide();
	        me.updateLayout();

	        me.fireEvent('clear', me);
	        clean_school();
	    },

	    updateValue: function() {
	        var me = this,
	            selectedRecords = me.valueCollection.getRange();

	        me.callParent();

	        if (selectedRecords.length > 0) {
	            me.getTrigger('clear').show();
	            me.updateLayout();
	        }
	    }
	});
	
    Ext.create('Ext.container.Viewport', {
        extend: 'Ext.panel.Panel',
        xtype: 'layout-border',
        requires: [
            'Ext.layout.container.Border'
        ],
        layout: 'border',
        width: "100%",
        height: 400,

        bodyBorder: false,
        
        defaults: {
            collapsible: true,
            split: true,
            bodyPadding: 10
        },
        items: [
        {
            title: 'Chart',
            region: 'south',
            height: "35%",
            minHeight: 75,
            //maxHeight: 150,
            html: '<div id="container" style="min-width: 300px; height: 100%; margin: 1em"></div>',
            tbar: [{
                xtype:'splitbutton',
                text:'Charts',
                iconCls: null,
                glyph: 61,
                menu:[{
                    text:'Column Chart',
                    listeners:{
                       click: function(){chart.type="column";chart.showChart();}
                    }
                },{
                    text:'Line Chart',
                    listeners:{
                       click: function(){chart.type="line";chart.showChart();}
                    }
                }]
            }]
        },
        {
            title: 'Navigation',
            region:'west',
            floatable: false,
            margin: '5 0 0 0',
            width: "30%",
            minWidth: "30%",
            maxWidth: "40%",
            scrollable: true,

            extend: 'Ext.tab.Panel',
            xtype: 'basic-tabs',
            controller: 'tab-view',
            

            defaults: {
                bodyPadding: 10,
                autoScroll: true
            },
            items: [{
                title: 'School',
                items: school_nav
            }, {
                title: 'District',
                items: district_nav
            }, {
                title: 'State',
                items: []
            }]
        },
        main
        ]
    });    
});
