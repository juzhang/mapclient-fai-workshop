Plugin Development
==================

The `MAP Client Manual <http://map-client.readthedocs.io/en/latest/manual/index.html>`_ provides thorough information on MAP Client plugin development.

- For a description of the key components of MAP Client plugins, please refer to the `MAP Plugins page <http://map-client.readthedocs.io/en/latest/manual/MAP-plugin.html>`_.

- To create a new plugins, please refer to the `Plugin Wizard page <http://map-client.readthedocs.io/en/latest/manual/MAP-plugin-wizard.html>`_.

Plugin Walkthrough
------------------

Let's take a look at how the key components of a simple plugin are implemented in real life. We will look at the `TRC Frame Selector Step <https://github.com/mapclient-plugins/trcframeselectorstep>`_ plugin. This step takes as input data from a TRC file and outputs the coordinates of each marker at a user-configured frame. You can view its source code on the Github website or you can clone the repository and view the source code locally.

Browse to ``trcframeselectorstep/mapclientplugins/trcframeselectorstep/step.py``. Every step must have a step.py which must contain a the step's class derived from ``mapclient.mountpoints.workflowstep.WorkflowStepMountPoint``, e.g.::

    class TRCFrameSelectorStep(WorkflowStepMountPoint):

In the class's ``__init__`` method, the step name, category, icon, ports, and default configurations are defined::
    
    def __init__(self, location):
        super(TRCFrameSelectorStep, self).__init__('TRC Frame Selector', location)
        self._configured = False
        self._category = 'Anthropometry'
        # icon
        self._icon = QtGui.QImage(':/trcframeselectorstep/images/trcframeselectoricon.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#trcdata'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'integer'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#landmarks'))

        # configuration defaults
        self._config = {}
        self._config['identifier'] = ''
        self._config['Frame'] = '1'

        # other private attributes of the step
        self._trcdata = None
        self._inputFrame = None
        self._landmarks = None

The ``execute`` method performs the main work of the step. In this case, it is extracting the marker coordinates at a particular frame::

    def execute(self):
        
        ...

        landmarksNames = self._trcdata['Labels']
        try:
            time, landmarksCoords = self._trcdata[frame]
        except KeyError:
            print('Frame {} not found'.format(frame))
            raise KeyError
            
        landmarksNamesData = [frame, time] + landmarksCoords
        self._landmarks = dict(zip(landmarksNames, landmarksNamesData))
        if 'Frame#' in self._landmarks:
            del self._landmarks['Frame#']
        if 'Time' in self._landmarks:
            del self._landmarks['Time']

        for k, v in self._landmarks.items():
            self._landmarks[k] = np.array(v)
        self._doneExecution()

In a simple plugin, all the "execution" code can be contained in the ``execute`` method. For more complicated steps however, we recommend creating a separate function, possibly in a separate module, that ``execute`` calls. The ``self._doneExecution()`` call at the end notifies the MAP Client that this step has finished execution.

The ``setPortData`` and ``getPortData`` methods assign and returns values to and from step class attributes, respectively::

    def setPortData(self, index, dataIn):
        if index == 0:
            self._trcdata = dataIn # trcdata
        else:
            self._inputFrame = dataIn # integer

    def getPortData(self, index):
        return self._landmarks # ju#landmarks

Ports (input and output combined) are numbered in the order they are defined in the ``__init__`` method.

The ``configure`` method launches a dialogue to accept user-defined configuration parameters::

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog(QtGui.QApplication.activeWindow().currentWidget())
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)
        
        if dlg.exec_():
            self._config = dlg.getConfig()
        
        self._configured = dlg.validate()
        self._configuredObserver()

The ``getIdentifier`` and ``setIdentifier`` methods allow MAP Client to set and get the name of the step::

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

These methods are automatically generated by the Plugin Wizard. No customiation is needed.

The ``serialize`` and ``deserialize`` methods allow the MAP Client to write step configurations to file and read them from file, respectively::

    def serialize(self):
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()

The step.py file along with the step class and the methods above are automatically generated by the `MAP Client Plugin Wizard <http://map-client.readthedocs.io/en/latest/manual/MAP-plugin-wizard.html>`_. For simple plugins, only the ``__init__``, ``execute``, ``getPortData``, and ``setPortData`` method need to be added to by the developer.


Writing some Simple Plugins
---------------------------

The `MAP Client Plugin Wizard <http://map-client.readthedocs.io/en/latest/manual/MAP-plugin-wizard.html>`_ helps writing new plugins by generating the boiler-plate code and folder structure for any plugins. We will use the Plugin Wizard to write two simple plugin.

1. Run MAP Client, go to *tools>Plugin Wizard*. Follow the steps `here <http://map-client.readthedocs.io/en/latest/manual/MAP-plugin-wizard.html>`__ to write a simple plugin called "Float Source" that outputs a user-configured float. The output port data type can be ``http://physiomeproject.org/workflow/1.0/rdf-schema#images``.

2. Run the Plugin wizard again. This time write a plugin called "Float Sum" that accepts two floats and prints to terminal and outputs their sum.

3. Create a new workflow to test these 2 plugins.