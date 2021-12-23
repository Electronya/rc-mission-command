import logging
import tkinter as tk


class UnitFrame(tk.LabelFrame):
    """
    The unit frame.
    """
    def __init__(self, parent, units, *args, **kwargs):
        """
        Contructor.

        Params:
            parent:         The parent of the frame.
            units:          The connected units.
        """
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)

        self._logger = logging.getLogger('UNIT_FRM')
        self._logger.debug('initializing the unit frame')

        self._parent = parent
        self._root = self._parent.nametowidget(self._parent.winfo_parent())
        self._units = units

        self._generate_unit_id_list()

        self._logger.debug(f"connected units: {self._unitIds}")

        self._unitIdsVar = tk.StringVar(value=self._unitIds)

        self._unitListbox = tk.Listbox(self, height=44, width=45,
                                       listvariable=self._unitIdsVar,
                                       selectmode='browse')
        self._unitListbox.grid(row=0, column=0, padx=10, pady=10)
        self._unitListbox.bind('<<ListboxSelect>>', self._select_unit)

        self._root.bind('<<update-unit>>', self._update_unit_list)

        self._logger.debug('initialization done')

    def _generate_unit_id_list(self):
        """
        Generate the unit ID list.
        """
        self._unitIds = []
        for unit in self._units['list']:
            self._unitIds.append(unit.get_id())

    def _select_unit(self, event):
        """
        The select unit event callback.
        """
        selectedUnit = self._unitListbox.get(tk.ACTIVE)
        self._logger.debug(f"changing active unit to {selectedUnit}")
        for unit in self._units['list']:
            if selectedUnit == unit.get_id():
                self._units['active'] = unit

    def _update_unit_list(self, event):
        """
        Update the unit list.
        """
        self._logger.debug('updating unit listbox')
        selectedUnit = self._unitListbox.get(tk.ACTIVE)
        self._generate_unit_id_list()
        self._unitIdsVar.set(self._unitIds)
        if selectedUnit not in self._unitIds:
            self._units['active'] = None
            self._logger.debug(f"active unit: {self._units['active']}")
