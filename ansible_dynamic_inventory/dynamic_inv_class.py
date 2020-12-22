""" ansible helper classes and functions


    Fri Jun 5 11:05:32 PM 2020

    __author__ = 'lima'

"""
import json


class DynInv:
    """ ansible dynamic inventory helper class

                import this.module as inv

                x = inv.DynInv()

                hosts = ["h1dc1", "h2dc1", "h3bdc", "h4dc1", "h5dc1"]

                for h in hosts:
                    x.add_host_to_group(host=h, grp_name=h[-3:])

                for h in hosts:
                    x.add_host_to_group(host=h, grp_name=h[-3:], grp_vars=ios_vars)

                for h in hosts:
                    x.add_host_to_group(host=h, grp_name="my_group_1", grp_vars=ios_vars)

                x.dump()
    """

    def __init__(self):
        self.inv = {"_meta": {"hostvars": {}}}
        self._ungrouped = self.add_group(grp_name="ungrouped")
        self._hostvars = self.inv["_meta"]["hostvars"]

    def chk_vars(self, my_vars: dict):
        """ checks vasrs and returns shallow copy """
        if my_vars:
            if isinstance(my_vars, dict):
                return my_vars.copy()
            else:
                raise TypeError(f"my_vars, not dict type, {type(my_vars)}")
        return {"ansible_connection": "network_cli"}

    def add_group(self, *, grp_name: str = None, grp_vars: dict = None):
        """ creates an ansible group with default values """
        my_vars = {"vars": self.chk_vars(grp_vars)}
        self.inv.setdefault(grp_name, {"hosts": []}).update(my_vars)
        return self.inv[grp_name]["hosts"]

    def add_host_to_group(
        self, *, host: str = None, grp_name: str = None, grp_vars: dict = None
    ):
        h, grp_name = str(host), grp_name or "NO_GRP_GIVEN"
        grp_hosts = self.add_group(grp_name=grp_name, grp_vars=grp_vars)
        if h not in grp_hosts:
            grp_hosts.append(h)
        if h not in self._ungrouped:
            self._ungrouped.append(h)
        return self._ungrouped, self.inv[grp_name]["hosts"]

    def update_group_vars(self, *, grp_name: str = None, grp_vars: dict = None):
        my_vars = self.chk_vars(grp_vars)
        self.inv[grp_name]["vars"].update(my_vars)
        return self.inv[grp_name]["vars"]

    def add_group_list(self, *, grp_list: list = None, grp_vars: dict = None):
        """ populate a list of ansible groups & group vars """
        my_vars = self.chk_vars(grp_vars)
        for group in grp_list:
            self.add_group(grp_name=group, grp_vars=my_vars)

    def update_host_vars(self, host: str, host_vars: dict = None):
        host, h_vars = str(host), self.chk_vars(host_vars)
        self._hostvars.setdefault(host, h_vars).update(h_vars)
        return self._hostvars.get(host, 0)

    def total_hosts(self):
        """ total number of unique ansible hosts """
        return len(self._ungrouped)

    def total_groups(self):
        """ total number of user defined ansible groups minus built ins groups """
        return len(self.inv.keys()) - 2

    def dump(self):
        """ dumps inventory in json format, ready for ansible """
        print(json.dumps(self.inv, indent=4))
