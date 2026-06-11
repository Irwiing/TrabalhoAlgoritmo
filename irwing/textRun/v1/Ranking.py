import os

class Ranking:
    def __init__(self, filename=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if filename is None:
            filename = os.path.join(base_dir, 'ranking.txt')
        elif not os.path.isabs(filename):
            filename = os.path.join(base_dir, filename)
        self.filename = filename
        self.rankings = []
        self.load_rankings()
    
    def load_rankings(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.rankings = []
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(',')
                            if len(parts) == 2:
                                name, score = parts
                                try:
                                    score = int(score)
                                except:
                                    continue
                                self.rankings.append({'name': name, 'score': score})
                    self.rankings.sort(key=lambda x: x['score'], reverse=True)
            except:
                self.rankings = []
        else:
            self.rankings = []
    
    def add_score(self, name, score):
        self.rankings.append({'name': name, 'score': score})
        self.rankings.sort(key=lambda x: x['score'], reverse=True)
        self.save_rankings()
    
    def save_rankings(self):
        dirpath = os.path.dirname(self.filename)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        with open(self.filename, 'w', encoding='utf-8') as f:
            for entry in self.rankings[:20]:
                f.write(f"{entry['name']},{entry['score']}\n")
    
    def get_top_10(self):
        return self.rankings[:10]
    
    def get_all_rankings(self):
        return self.rankings
