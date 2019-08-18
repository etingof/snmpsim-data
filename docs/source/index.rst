
SNMP simulation data
====================

.. toctree::
   :maxdepth: 2

Free and open-source `SNMP agent simulator <http://snmplabs.com/snmpsim>`_ pretends to be one
or many SNMP agents. To be a reasonably convincing SNMP agent, simulator needs to serve SNMP
managed objects that resemble the ones served by real-world SNMP-enabled devices.

This is a collection of snapshots taken from various hardware devices and operating systems.

The data snapshots are distributed under 2-clause :doc:`BSD license </license>`.

On-line simulation
------------------

All the packaged snapshots are served by
`public SNMP simulator instance <http://demo.snmplabs.com>`_ under SNMP community and
Context Name identifiers noted in the documentation below.

For example, to read SNMP managed object of the Ubiquiti M5 Wi-Fi bridge:

.. code-block:: bash

   $ snmpget -v2c -c network/wifi/ubiquiti-m5 sysDescr.0 demo.snmplabs.com

Local simulation
----------------

If you prefer to have local simulation, follow `SNMP simulator documentation <http://snmplabs.com/snmpsim>`_
on how to set up simulation data. Besides other things, local installation will let you
add data variation calls into the otherwise static snapshots.

Snapshots contribution
----------------------

Consider donating some snapshots of SNMP data (e.g. snmpwalk) as reported by any real-world hardware to the SNMP simulator project. Having the real-world SNMP probes would benefit many SNMP implementers and testers.

Technically, it can be a PR against snmpsim-data package adding your .snmpwalk or .snmprec files to the data directory. Or a URL to download. Or any other way.

Just keep in mind that your SNMP dumps may contain sensitive information. Therefore it's best to snmpwalk non-production devices.

With your permission, we would then publish these snmpwalk's online.

Simulation data inventory
-------------------------

.. toctree::
   :maxdepth: 2
   :glob:

   /data/*

