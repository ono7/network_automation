""" Filters for interacting sqlite

    Fri May 22 8:34:17 PM 2020

    __author__ = 'Jose Lima'

    sqlite sauce:
        if update does not happen Select Changes() = 0, lets insert instead, incase
        sqlite3 ver < 3.24.x without UPSERT support, this removes sqlite version dependencies


    takes show arp from switch and does some "magic", logs to sqlite db for reporting

"""
# TODO: fix mac_type updates,  05-26-2020 06:19 PM CDT
import sqlite3
import re

dot1x_regex = re.compile(r"(\S+)\s+\b(\w{4}\.\w{4}\.\w{4})\b\s+(\S+).*")

mac_regex = re.compile(
    r"^.*\b(\d{1,4})\s+\b(\w{4}\.\w{4}\.\w{4})\b\s+\b(?!DYNAMIC)(\S+).*\b(?!Te|Po)([A-Z]\S+\d)$"
)

arp_regex = re.compile(
    r"^.*\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b.*\b(\w{4}\.\w{4}\.\w{4})\b.*\b(\S+)$"
)

create_table = """
CREATE TABLE IF NOT EXISTS records (mac TEXT PRIMARY KEY ON CONFLICT IGNORE,
    site TEXT DEFAULT '', arp_rtr TEXT DEFAULT '', rtr_int TEXT DEFAULT '',
    ip TEXT DEFAULT '', l2_switch TEXT DEFAULT '', vlan TEXT DEFAULT '',
    mac_type TEXT DEFAULT '', connected_to TEXT DEFAULT '', dot1x TEXT DEFAULT 'no dot1x');
"""

arp_sql_insert = """
INSERT INTO records(ip,site,arp_rtr,rtr_int) SELECT ?,?,?,?
    WHERE (Select Changes() = 0)
"""
arp_sql_update = """
UPDATE records SET ip = ?, rtr_int = ?, arp_rtr = ?
    WHERE mac = ?
"""

mac_sql_update = """
UPDATE records SET vlan = ?, connected_to = ?, mac_type = ?, l2_switch = ?
    WHERE mac = ? AND mac_type != 'static'
"""
mac_sql_insert = """
INSERT INTO records(vlan,mac,connected_to,l2_switch,site,mac_type) SELECT ?,?,?,?,?,?
    WHERE (Select Changes() = 0)
"""

dot1x_sql_insert = """
INSERT INTO records(mac,dot1x,l2_switch,site,connected_to) SELECT ?,?,?,?,?
    WHERE (Select Changes() = 0)
"""
dot1x_sql_update = """
UPDATE records SET dot1x = ?, connected_to = ?, l2_switch = ?, site = ?
    WHERE mac = ?
"""


class FilterModule:
    """ datbase ansible filter """

    def filters(self):
        return {
            "sql_init_db": self.sql_init_db,
            "sql_arp_bindings": self.sql_arp_bindings,
            "sql_mac_tables": self.sql_mac_tables,
            "sql_dot1x_status": self.sql_dot1x_status,
        }

    @staticmethod
    def get_db():
        """ return sql lite connection """
        c = sqlite3.connect("results.db", isolation_level=None)
        c.execute("pragma journal_mode=wal;")
        return c

    def sql_init_db(self, dbname):
        """ initialize database schema """
        dbname = "results.db"
        c = sqlite3.connect(dbname)
        c.execute(create_table)
        c.close()
        return ""

    def sql_arp_bindings(self, arp_rtr, data, site):
        c = self.get_db()
        try:
            for line in data:
                m = arp_regex.search(line.strip())
                if m:
                    ip, mac, rtr_int = m.groups()
                    update = (f"{ip}", f"{rtr_int}", f"{arp_rtr}", f"{mac}")
                    insert = (f"{ip}", f"{site}", f"{arp_rtr}", f"{rtr_int}")
                    c.execute(arp_sql_update, update)
                    c.execute(arp_sql_insert, insert)
        finally:
            c.close()
        return ""

    def sql_mac_tables(self, l2_switch, site, data):
        c = self.get_db()
        try:
            for line in data:
                m = mac_regex.search(line.strip())
                if m:
                    vlan, mac, mac_type, connected_to = m.groups()
                    updates = (
                        f"{vlan}",
                        f"{connected_to}",
                        f"{mac_type.lower()}",
                        f"{l2_switch}",
                        f"{mac}",
                    )
                    inserts = (
                        f"{vlan}",
                        f"{mac}",
                        f"{connected_to}",
                        f"{l2_switch}",
                        f"{site}",
                        f"{mac_type.lower()}",
                    )
                    c.execute(mac_sql_update, updates)
                    c.execute(mac_sql_insert, inserts)
        finally:
            c.close()
        return ""

    def sql_dot1x_status(self, l2_switch, site, data):
        c = self.get_db()
        try:
            for line in data:
                m = dot1x_regex.search(line.strip())
                if m:
                    connected_to, mac, dot1x = m.groups()
                    updates = (
                        f"{dot1x}",
                        f"{connected_to}",
                        f"{l2_switch}",
                        f"{site}",
                        f"{mac}",
                    )
                    inserts = (
                        f"{mac}",
                        f"{dot1x}",
                        f"{l2_switch}",
                        f"{site}",
                        f"{connected_to}",
                    )
                    c.execute(dot1x_sql_update, updates)
                    c.execute(dot1x_sql_insert, inserts)
        finally:
            c.close()
        return ""
