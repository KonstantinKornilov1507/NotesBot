import pickle
class BotObjects(object):

    def __init__(self):

        self.Notes_of_Ussers = dict()
        self.Registration_dict = dict()
        self.Append_Name = dict()
        self.Nick = dict()

    def create_user(self, id):
        self.Notes_of_Ussers[id] = dict()
        self.Registration_dict[id] = list()

    def set_privacy(self,pr,id):
        self.Registration_dict[id].append(pr)

    def registration(self, id, nick):
        self.Registration_dict[id].append(nick)
        self.Nick[nick] = id

    def make_note(self, name, txt, id):
        self.Notes_of_Ussers[id][name] = txt

    def Userlen(self, id):
        return len(self.Notes_of_Ussers[id])

    def delete_note(self, id, name):
        del self.Notes_of_Ussers[id][name]

    def nick_to_share(self, id):
        list = []
        for i in self.Registration_dict.keys():
            if i != id and self.Registration_dict[i][1] == "public":
                list.append(self.Registration_dict[i][0])
        return list

    def sharing(self, list, note_to_share):
        for i in self.Nick.keys():
            if list[1] == i:
                share_id = self.Nick[i]
        self.Notes_of_Ussers[share_id][list[0]] = note_to_share

    def change(self, id, new_note, name_of_note):
        self.Notes_of_Ussers[id][name_of_note] = new_note

    def Delete(self, id):
        x = self.Notes_of_Ussers.pop(id)
        y = self.Registration_dict.pop(id)
        for i in self.Nick.keys():
            if self.Nick[i] == id:
                s = i
        self.Nick.pop(s)