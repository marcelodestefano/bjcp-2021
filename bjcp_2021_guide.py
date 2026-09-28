#!/usr/bin/env python3
"""
BJCP 2021 Style Guide - Engine de Pesquisa e Estudo de Parâmetros
=================================================================
Este módulo provê uma estrutura de dados orientada a objetos (Python Dataclasses)
e um mecanismo de busca e filtragem para os parâmetros do Guia de Estilos de Cerveja
BJCP 2021 (Beer Judge Certification Program).

Projeto estruturado para repositórios GitHub de estudo cervejeiro e automação.
"""

import json
import argparse
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class VitalStats:
    """Estatísticas Vitais (Parâmetros Físico-Químicos) de um Estilo BJCP."""
    og_min: Optional[float] = None
    og_max: Optional[float] = None
    fg_min: Optional[float] = None
    fg_max: Optional[float] = None
    ibu_min: Optional[float] = None
    ibu_max: Optional[float] = None
    srm_min: Optional[float] = None
    srm_max: Optional[float] = None
    abv_min: Optional[float] = None
    abv_max: Optional[float] = None

    def match_range(
        self,
        og: Optional[float] = None,
        fg: Optional[float] = None,
        ibu: Optional[float] = None,
        srm: Optional[float] = None,
        abv: Optional[float] = None,
    ) -> bool:
        """Verifica se determinados valores numéricos estão dentro dos intervalos aceitos pelo estilo."""
        if og is not None and (self.og_min is not None and self.og_max is not None):
            if not (self.og_min <= og <= self.og_max):
                return False
        if fg is not None and (self.fg_min is not None and self.fg_max is not None):
            if not (self.fg_min <= fg <= self.fg_max):
                return False
        if ibu is not None and (self.ibu_min is not None and self.ibu_max is not None):
            if not (self.ibu_min <= ibu <= self.ibu_max):
                return False
        if srm is not None and (self.srm_min is not None and self.srm_max is not None):
            if not (self.srm_min <= srm <= self.srm_max):
                return False
        if abv is not None and (self.abv_min is not None and self.abv_max is not None):
            if not (self.abv_min <= abv <= self.abv_max):
                return False
        return True


@dataclass
class BeerStyle:
    """Modelo completo para um Estilo do Guia BJCP 2021."""
    code: str
    name: str
    category_number: int
    category_name: str
    overall_impression: str
    stats: VitalStats
    tags: List[str] = field(default_factory=list)
    commercial_examples: List[str] = field(default_factory=list)
    ingredients: str = ""
    history: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BJCP2021Database:
    """Gerenciador e Motor de Busca do Guia BJCP 2021."""

    def __init__(self):
        self.styles: Dict[str, BeerStyle] = {}
        self._load_default_database()

    def add_style(self, style: BeerStyle):
        self.styles[style.code.upper()] = style

    def get_style(self, code: str) -> Optional[BeerStyle]:
        return self.styles.get(code.upper())

    def search_by_keyword(self, query: str) -> List[BeerStyle]:
        """Busca textual abrangente por palavra-chave."""
        q = query.lower().strip()
        results = []
        for style in self.styles.values():
            corpus = f"{style.code} {style.name} {style.category_name} {style.overall_impression} {style.ingredients} {style.history} {' '.join(style.commercial_examples)}".lower()
            if q in corpus:
                results.append(style)
        return results

    def filter_by_stats(
        self,
        og: Optional[float] = None,
        fg: Optional[float] = None,
        ibu: Optional[float] = None,
        srm: Optional[float] = None,
        abv: Optional[float] = None,
    ) -> List[BeerStyle]:
        """Filtra estilos cujos parâmetros físico-químicos contêm os valores fornecidos."""
        results = []
        for style in self.styles.values():
            if style.stats.match_range(og=og, fg=fg, ibu=ibu, srm=srm, abv=abv):
                results.append(style)
        return results

    def filter_by_tags(self, tags: List[str], match_all: bool = False) -> List[BeerStyle]:
        """Filtra estilos através de etiquetas oficiais do BJCP (ex: 'hoppy', 'sour', 'wheat-beer-family')."""
        req_tags = [t.lower().strip() for t in tags]
        results = []
        for style in self.styles.values():
            style_tags = [t.lower().strip() for t in style.tags]
            if match_all:
                if all(t in style_tags for t in req_tags):
                    results.append(style)
            else:
                if any(t in style_tags for t in req_tags):
                    results.append(style)
        return results

    def export_to_json(self, filepath: str):
        """Exporta o banco de dados em formato JSON estandardizado."""
        data = [s.to_dict() for s in self.styles.values()]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_default_database(self):
        """Popula o banco com uma amostragem representativa das categorias do BJCP 2021."""
        raw_styles = [
            # Categoria 1: Standard American Beer
            BeerStyle(
                code="1A",
                name="American Light Lager",
                category_number=1,
                category_name="Standard American Beer",
                overall_impression="Uma lager muito clara, altamente carbonatada, de corpo baixo e bem atenuada, com sabor neutro e baixo amargor.",
                stats=VitalStats(og_min=1.028, og_max=1.040, fg_min=0.998, fg_max=1.008, ibu_min=8, ibu_max=12, srm_min=2, srm_max=3, abv_min=2.8, abv_max=4.2),
                tags=["balanced", "bottom-fermented", "lagered", "north-america", "pale-color", "pale-lager-family", "session-strength", "traditional-style"],
                commercial_examples=["Bud Light", "Coors Light", "Michelob Light", "Miller Lite"],
                ingredients="Malte de cevada de duas ou seis fileiras com alta porcentagem de arroz ou milho como adjunto.",
                history="Desenvolvida em meados do século XX para atender consumidores que buscavam uma cerveja menos calórica e extremamente refrescante."
            ),
            BeerStyle(
                code="1B",
                name="American Lager",
                category_number=1,
                category_name="Standard American Beer",
                overall_impression="Uma cerveja lager muito clara, altamente carbonatada, de corpo baixo, bem atenuada, com um sabor neutro e baixo amargor.",
                stats=VitalStats(og_min=1.040, og_max=1.050, fg_min=1.004, fg_max=1.010, ibu_min=8, ibu_max=18, srm_min=2, srm_max=3.5, abv_min=4.2, abv_max=5.3),
                tags=["balanced", "bottom-fermented", "lagered", "north-america", "pale-color", "pale-lager-family", "standard-strength", "traditional-style"],
                commercial_examples=["Budweiser", "Coors Original", "Miller High Life", "Pabst Blue Ribbon"],
                ingredients="Malte de cevada com até 40% de arroz ou milho como adjuntos. Levedura lager limpa.",
                history="Evolução pós-Lei Seca e pós-Segunda Guerra Mundial das lagers americanas artesanais mais antigas."
            ),
            BeerStyle(
                code="1C",
                name="Cream Ale",
                category_number=1,
                category_name="Standard American Beer",
                overall_impression="Uma cerveja americana 'para o verão', saborosa, limpa, bem atenuada e altamente carbonatada.",
                stats=VitalStats(og_min=1.042, og_max=1.055, fg_min=1.006, fg_max=1.012, ibu_min=8, ibu_max=20, srm_min=2, srm_max=5, abv_min=4.2, abv_max=5.6),
                tags=["any-fermentation", "balanced", "north-america", "pale-ale-family", "pale-color", "standard-strength", "traditional-style"],
                commercial_examples=["Genesee Cream Ale", "Little Kings Cream Ale", "Sleeman Cream Ale"],
                ingredients="Malte americano de seis fileiras, até 20% de milho na mostura e açúcar na fervura.",
                history="Criada na segunda metade do século XIX nos EUA para competir com as lagers canadenses e alemãs."
            ),
            BeerStyle(
                code="1D",
                name="American Wheat Beer",
                category_number=1,
                category_name="Standard American Beer",
                overall_impression="Uma cerveja de trigo clara, refrescante, com notas de cereais, pão e massa de pão crua, com perfil de fermentação limpo.",
                stats=VitalStats(og_min=1.040, og_max=1.055, fg_min=1.008, fg_max=1.013, ibu_min=15, ibu_max=30, srm_min=3, srm_max=6, abv_min=4.0, abv_max=5.5),
                tags=["any-fermentation", "balanced", "craft-style", "north-america", "pale-color", "standard-strength", "wheat-beer-family"],
                commercial_examples=["Bell's Oberon", "Boulevard Unfiltered Wheat Beer", "Goose Island 312 Urban Wheat Ale"],
                ingredients="30-50% de malte de trigo, levedura ale neutra (sem banana e cravo alemães), lúpulos americanos.",
                history="Adaptação das cervejas de trigo alemãs por cervejarias artesanais americanas na década de 1980."
            ),
            # Categoria 3: Czech Lager
            BeerStyle(
                code="3B",
                name="Czech Premium Pale Lager",
                category_number=3,
                category_name="Czech Lager",
                overall_impression="Uma lager tcheca clara e refrescante com considerável caráter de malte e lúpulo (Saaz) e final prolongado.",
                stats=VitalStats(og_min=1.044, og_max=1.060, fg_min=1.013, fg_max=1.017, ibu_min=30, ibu_max=45, srm_min=3.5, srm_max=6, abv_min=4.2, abv_max=5.8),
                tags=["balanced", "bottom-fermented", "central-europe", "hoppy", "lagered", "pale-color", "pilsner-family", "standard-strength", "traditional-style"],
                commercial_examples=["Pilsner Urquell", "Budvar 33 svetlý ležák", "Bernard Svátecní ležák"],
                ingredients="Malte Pilsner tcheco, água de baixíssima mineralização, lúpulo Saaz (Žatec), fermentação lager.",
                history="Desenvolvida originalmente em Plzeň (Pilsen) por Josef Groll em 1842."
            ),
            # Categoria 5: Pale Bitter European Beer
            BeerStyle(
                code="5D",
                name="German Pils",
                category_number=5,
                category_name="Pale Bitter European Beer",
                overall_impression="Uma lager alemã clara, límpida, altamente atenuada, amarga e bem definida (crisp), enfatizando o aroma e sabor dos lúpulos nobres.",
                stats=VitalStats(og_min=1.044, og_max=1.050, fg_min=1.008, fg_max=1.013, ibu_min=22, ibu_max=40, srm_min=2, srm_max=4, abv_min=4.4, abv_max=5.2),
                tags=["bitter", "bottom-fermented", "central-europe", "hoppy", "lagered", "pale-color", "pilsner-family", "standard-strength", "traditional-style"],
                commercial_examples=["Bitburger Premium Pils", "Jever Pilsener", "König Pilsener", "Rothaus Pils"],
                ingredients="Malte Pilsner continental, lúpulos alemães nobres (Hallertau, Tettnang, Spalt), levedura lager atenuante.",
                history="Adaptação alemã da Pilsner tcheca a partir dos anos 1870 com água mais dura e perfil mais seco e amargo."
            ),
            # Categoria 6: Amber Malty European Lager
            BeerStyle(
                code="6A",
                name="Märzen",
                category_number=6,
                category_name="Amber Malty European Lager",
                overall_impression="Uma cerveja lager alemã de cor âmbar com sabor de malte limpo, rico, tostado, como pão, amargor contido e final bem atenuado.",
                stats=VitalStats(og_min=1.054, og_max=1.060, fg_min=1.010, fg_max=1.014, ibu_min=18, ibu_max=24, srm_min=8, srm_max=17, abv_min=5.6, abv_max=6.3),
                tags=["amber-color", "amber-lager-family", "bottom-fermented", "central-europe", "lagered", "malty", "standard-strength", "traditional-style"],
                commercial_examples=["Hacker-Pschorr Oktoberfest Märzen", "Paulaner Oktoberfest", "Weltenburg Kloster Anno 1050"],
                ingredients="Maltes Munich, Vienna e Pilsner, brassagem por decocção tradicional, lúpulos alemães.",
                history="Produzida em março como cerveja de guarda para o verão europeu e servida na Oktoberfest de Munique de 1872 a 1990."
            ),
            # Categoria 10: German Wheat Beer
            BeerStyle(
                code="10A",
                name="Weissbier",
                category_number=10,
                category_name="German Wheat Beer",
                overall_impression="Uma cerveja de trigo alemã clara e refrescante com alta carbonatação, final seco, sensação na boca frutada e perfil característico de banana e cravo.",
                stats=VitalStats(og_min=1.044, og_max=1.053, fg_min=1.008, fg_max=1.014, ibu_min=8, ibu_max=15, srm_min=2, srm_max=6, abv_min=4.3, abv_max=5.6),
                tags=["central-europe", "malty", "pale-color", "standard-strength", "top-fermented", "traditional-style", "wheat-beer-family"],
                commercial_examples=["Ayinger Bräu Weisse", "Hacker-Pschorr Hefeweißbier", "Paulaner Hefe-Weißbier", "Weihenstephaner Hefeweissbier"],
                ingredients="Pelo menos 50% malte de trigo, malte Pilsner, levedura Weizen de alta fermentação geradora de isoamil acetato (banana) e 4-vinil-guiacol (cravo).",
                history="Estilo tradicional da Baviera cuja produção já foi um privilégio exclusivo da nobreza bávara."
            ),
            # Categoria 11: British Bitter
            BeerStyle(
                code="11C",
                name="Strong Bitter",
                category_number=11,
                category_name="British Bitter",
                overall_impression="Uma cerveja britânica amarga de força média a moderadamente forte, com equilíbrio entre maltes complexos, ésteres e lúpulos terrosos.",
                stats=VitalStats(og_min=1.048, og_max=1.060, fg_min=1.010, fg_max=1.016, ibu_min=30, ibu_max=50, srm_min=8, srm_max=18, abv_min=4.6, abv_max=6.2),
                tags=["amber-ale-family", "amber-color", "bitter", "british-isles", "session-strength", "top-fermented", "traditional-style"],
                commercial_examples=["Bass Ale", "Fuller's ESB", "Samuel Smith's Organic Pale Ale", "Shepherd Neame Bishop's Finger"],
                ingredients="Maltes Pale Ale, Amber, Crystal. Lúpulos ingleses de adição tardia (EKG, Fuggles), levedura britânica esterificada.",
                history="Evoluiu como uma versão de alta densidade da família das Bitters britânicas."
            ),
            # Categoria 13: Brown British Beer
            BeerStyle(
                code="13C",
                name="English Porter",
                category_number=13,
                category_name="Brown British Beer",
                overall_impression="Uma cerveja inglesa marrom escura, de teor alcoólico moderado, com caráter amargo e torrado contido, destacando chocolate e caramelo.",
                stats=VitalStats(og_min=1.040, og_max=1.052, fg_min=1.008, fg_max=1.014, ibu_min=18, ibu_max=35, srm_min=20, srm_max=30, abv_min=4.0, abv_max=5.4),
                tags=["british-isles", "dark-color", "malty", "porter-family", "roasty", "standard-strength", "top-fermented", "traditional-style"],
                commercial_examples=["Fuller's London Porter", "Samuel Smith Taddy Porter", "Bateman's Salem Porter"],
                ingredients="Maltes pale, crystal e chocolate/black. Lúpulos ingleses e levedura de ale britânica.",
                history="Desenvolvida em Londres no início do século XVIII como bebida da classe trabalhadora e carregadores (porters)."
            ),
            # Categoria 15: Irish Beer
            BeerStyle(
                code="15B",
                name="Irish Stout",
                category_number=15,
                category_name="Irish Beer",
                overall_impression="Uma cerveja preta com sabor torrado pronunciado, semelhante a café, final seco e amargor de moderado a alto.",
                stats=VitalStats(og_min=1.036, og_max=1.044, fg_min=1.007, fg_max=1.011, ibu_min=25, ibu_max=45, srm_min=25, srm_max=40, abv_min=4.0, abv_max=4.5),
                tags=["bitter", "british-isles", "dark-color", "roasty", "session-strength", "stout-family", "top-fermented", "traditional-style"],
                commercial_examples=["Guinness Draught", "Murphy's Irish Stout", "Beamish Irish Stout", "O'Hara's Leann Folláin"],
                ingredients="Cevada torrada não maltada, malte pale, cevada em flocos, amargor assertivo de lúpulo.",
                history="Evolução das Porters mais fortes na Irlanda durante o século XIX, imortalizada pela cervejaria St. James's Gate da Guinness."
            ),
            # Categoria 21: IPA
            BeerStyle(
                code="21A",
                name="American IPA",
                category_number=21,
                category_name="IPA",
                overall_impression="Uma cerveja americana clara, com teor alcoólico moderadamente alto, incontestavelmente lupulada e amarga, com perfil de fermentação limpo e final seco.",
                stats=VitalStats(og_min=1.056, og_max=1.070, fg_min=1.008, fg_max=1.014, ibu_min=40, ibu_max=70, srm_min=6, srm_max=14, abv_min=5.5, abv_max=7.5),
                tags=["bitter", "craft-style", "high-strength", "hoppy", "ipa-family", "north-america", "pale-color", "top-fermented"],
                commercial_examples=["Bell's Two-Hearted Ale", "Cigar City Jai Alai", "Firestone Walker Union Jack", "Russian River Blind Pig IPA"],
                ingredients="Malte base Pale, pouca utilização de maltes crystal, lúpulos americanos/Novo Mundo cítricos/resinosos/tropicais, levedura ale limpa.",
                history="Pioneira com a Anchor Liberty Ale (1975), tornou-se o estilo símbolo da revolução da cerveja artesanal americana."
            ),
            BeerStyle(
                code="21C",
                name="Hazy IPA",
                category_number=21,
                category_name="IPA",
                overall_impression="Uma IPA americana com sabores e aromas intensos de frutas tropicais, corpo macio e aveludado, aparência opaca/turva e menor amargor perceptível.",
                stats=VitalStats(og_min=1.060, og_max=1.085, fg_min=1.010, fg_max=1.015, ibu_min=25, ibu_max=60, srm_min=3, srm_max=7, abv_min=6.0, abv_max=9.0),
                tags=["bitter", "craft-style", "high-strength", "hoppy", "ipa-family", "north-america", "pale-color", "top-fermented"],
                commercial_examples=["Tree House Julius", "Trillium Congress Street", "WeldWerks Juicy Bits", "Hill Farmstead Susan"],
                ingredients="Maltes claros, aveia/trigo em flocos, carga maciça de dry-hopping na fermentação ativa, levedura esterificada.",
                history="Originada na região da Nova Inglaterra (New England/NEIPA) nos EUA durante a década de 2010."
            ),
            # Categoria 22: Strong American Ale
            BeerStyle(
                code="22A",
                name="Double IPA",
                category_number=22,
                category_name="Strong American Ale",
                overall_impression="Uma ale clara com teor alcoólico mais alto, amarga e intensamente lupulada, sem o corpo pesado ou dulçor de uma Barleywine.",
                stats=VitalStats(og_min=1.065, og_max=1.085, fg_min=1.008, fg_max=1.018, ibu_min=60, ibu_max=100, srm_min=6, srm_max=14, abv_min=7.5, abv_max=10.0),
                tags=["bitter", "craft-style", "hoppy", "ipa-family", "north-america", "pale-color", "top-fermented", "very-high-strength"],
                commercial_examples=["Russian River Pliny the Elder", "Stone Ruination Double IPA", "Fat Head's Hop Juju"],
                ingredients="Malte pilsner ou pale neutro, açúcar de cana/dextrose para secura, múltiplas adições de lúpulo americano.",
                history="Desenvolvida nos EUA meados dos anos 1990 (ex: Vinny Cilurzo na Blind Pig / Russian River)."
            ),
            # Categoria 23: European Sour Ale
            BeerStyle(
                code="23A",
                name="Berliner Weisse",
                category_number=23,
                category_name="European Sour Ale",
                overall_impression="Uma cerveja de trigo alemã muito clara, refrescante, de baixo teor alcoólico, com uma acidez lática limpa e alto nível de carbonatação.",
                stats=VitalStats(og_min=1.028, og_max=1.032, fg_min=1.003, fg_max=1.006, ibu_min=3, ibu_max=8, srm_min=2, srm_max=3, abv_min=2.8, abv_max=3.8),
                tags=["central-europe", "pale-color", "session-strength", "sour", "top-fermented", "traditional-style", "wheat-beer-family"],
                commercial_examples=["Bayerischer Bahnhof Berliner Style Weisse", "Lemke Berlin Budike Weisse"],
                ingredients="Malte Pilsner e malte de trigo (50%+), co-fermentação com levedura ale e Lactobacillus.",
                history="Especialidade regional de Berlim chamada pelas tropas napoleônicas de 'A Champanhe do Norte' em 1809."
            ),
            # Categoria 25: Strong Belgian Ale
            BeerStyle(
                code="25B",
                name="Saison",
                category_number=25,
                category_name="Strong Belgian Ale",
                overall_impression="Uma ale belga artesanal de fazenda (farmhouse ale) altamente atenuada, lupulada, bem seca, frutada e picante de levedura.",
                stats=VitalStats(og_min=1.048, og_max=1.065, fg_min=1.002, fg_max=1.008, ibu_min=20, ibu_max=35, srm_min=5, srm_max=14, abv_min=5.0, abv_max=7.0),
                tags=["bitter", "pale-color", "standard-strength", "top-fermented", "traditional-style", "western-europe"],
                commercial_examples=["Saison Dupont", "Boulevard Tank 7 Farmhouse Ale", "Saison de Pipaix"],
                ingredients="Malte pilsner, grãos não malteados (trigo, espelta, aveia), lúpulos continentais, levedura Saison atenuante.",
                history="Cerveja tradicionalmente produzida nas fazendas da Valônia (Bélgica) para saciar a sede dos trabalhadores durante as colheitas."
            ),
            # Categoria 26: Monastic Ale
            BeerStyle(
                code="26C",
                name="Belgian Tripel",
                category_number=26,
                category_name="Monastic Ale",
                overall_impression="Uma cerveja belga forte, clara, levemente condimentada, com sabor arredondado de malte, amargor assertivo e final seco.",
                stats=VitalStats(og_min=1.075, og_max=1.085, fg_min=1.008, fg_max=1.014, ibu_min=20, ibu_max=40, srm_min=4.5, srm_max=7, abv_min=7.5, abv_max=9.5),
                tags=["bitter", "high-strength", "pale-color", "top-fermented", "traditional-style", "western-europe"],
                commercial_examples=["Westmalle Tripel", "Chimay Tripel", "La Trappe Tripel", "St. Bernardus Tripel"],
                ingredients="Malte Pilsner belga, açúcar claro para efervescência e secura, lúpulos Saaz/Styrian Goldings, levedura de abadia.",
                history="Popularizada no mosteiro de Westmalle em 1931."
            ),
            # Apêndice B: Estilos Locais (Brasil)
            BeerStyle(
                code="X4",
                name="Catharina Sour",
                category_number=99,
                category_name="Apêndice B: Estilos Locais (Brasil)",
                overall_impression="Uma cerveja brasileira de trigo refrescante, ácida, de corpo leve e carbonatação elevada, destacando o caráter vívido de fruta fresca.",
                stats=VitalStats(og_min=1.039, og_max=1.048, fg_min=1.004, fg_max=1.012, ibu_min=2, ibu_max=8, srm_min=2, srm_max=6, abv_min=4.0, abv_max=5.5),
                tags=["craft-style", "fruit", "sour", "specialty-beer", "south-america"],
                commercial_examples=["Blumenau Catharina Sour Pêssego", "Armada Daenerys", "Itajahy Catharina Araçá Sour"],
                ingredients="Malte Pilsen e Wheat, técnica Kettle Sour com Lactobacillus, fruta fresca tropical adicionada na fermentação.",
                history="Criada em Santa Catarina (Brasil) em 2015 por cervejeiros artesanais e caseiros locais."
            )
        ]
        for style in raw_styles:
            self.add_style(style)


def cli():
    parser = argparse.ArgumentParser(description="Mecanismo de Pesquisa do Guia BJCP 2021")
    parser.add_argument("--search", type=str, help="Termo para busca textual (nome, ingredientes, descrição)")
    parser.add_argument("--abv", type=float, help="Filtrar estilos compátiveis com determinado teor alcoólico (% vol)")
    parser.add_argument("--ibu", type=float, help="Filtrar estilos compatíveis com determinado nível de amargor (IBU)")
    parser.add_argument("--srm", type=float, help="Filtrar estilos compatíveis com determinada cor (SRM)")
    parser.add_argument("--tag", type=str, help="Filtrar por tags separadas por vírgula (ex: sour,hoppy)")
    parser.add_argument("--code", type=str, help="Buscar por código exato (ex: 21A, 26C, X4)")
    parser.add_argument("--export", type=str, help="Caminho do arquivo JSON para exportação")
    parser.add_argument("--demo", action="store_true", help="Executar demonstração completa de consultas")

    args = parser.parse_args()
    db = BJCP2021Database()

    if args.export:
        db.export_to_json(args.export)
        print(f"[OK] Banco BJCP 2021 exportado com sucesso para '{args.export}'")
        return

    if args.code:
        style = db.get_style(args.code)
        if style:
            print(f"\n--- Detalhes do Estilo [{style.code}] {style.name} ---")
            print(f"Categoria: {style.category_number}. {style.category_name}")
            print(f"Impressão Geral: {style.overall_impression}")
            print(f"Estatísticas Vitais: OG ({style.stats.og_min}-{style.stats.og_max}), FG ({style.stats.fg_min}-{style.stats.fg_max}), IBU ({style.stats.ibu_min}-{style.stats.ibu_max}), SRM ({style.stats.srm_min}-{style.stats.srm_max}), ABV ({style.stats.abv_min}%-{style.stats.abv_max}%)")
            print(f"Tags: {', '.join(style.tags)}")
            print(f"Exemplos Comerciais: {', '.join(style.commercial_examples)}")
            print(f"Ingredientes: {style.ingredients}")
            print(f"História: {style.history}\n")
        else:
            print(f"[!] Estilo '{args.code}' não encontrado.")
        return

    if args.search:
        results = db.search_by_keyword(args.search)
        print(f"\n=== Resultados para busca '{args.search}' ({len(results)} encontrados) ===")
        for s in results:
            print(f"[{s.code}] {s.name} ({s.category_name})")
        return

    if args.abv is not None or args.ibu is not None or args.srm is not None:
        results = db.filter_by_stats(abv=args.abv, ibu=args.ibu, srm=args.srm)
        print(f"\n=== Estilos compatíveis com ABV={args.abv}, IBU={args.ibu}, SRM={args.srm} ({len(results)} encontrados) ===")
        for s in results:
            print(f"[{s.code}] {s.name} | ABV: {s.stats.abv_min}%-{s.stats.abv_max}% | IBU: {s.stats.ibu_min}-{s.stats.ibu_max} | SRM: {s.stats.srm_min}-{s.stats.srm_max}")
        return

    if args.tag:
        tags = [t.strip() for t in args.tag.split(",")]
        results = db.filter_by_tags(tags)
        print(f"\n=== Estilos com as tags '{args.tag}' ({len(results)} encontrados) ===")
        for s in results:
            print(f"[{s.code}] {s.name} ({s.category_name})")
        return

    # Se nenhum argumento ou --demo for passado
    print("=== GUIA DE ESTILOS BJCP 2021 - MECANISMO DE CONSULTA E ESTUDO ===")
    print(f"Base de dados carregada com {len(db.styles)} estilos de referência.\n")

    print("--- 1. Exemplo de Busca por Parâmetros (Ex: ABV 6.0%, IBU 50) ---")
    param_matches = db.filter_by_stats(abv=6.0, ibu=50)
    for s in param_matches:
        print(f" -> [{s.code}] {s.name} (ABV: {s.stats.abv_min}-{s.stats.abv_max}%, IBU: {s.stats.ibu_min}-{s.stats.ibu_max})")

    print("\n--- 2. Exemplo de Busca por Tag 'sour' ---")
    sour_matches = db.filter_by_tags(["sour"])
    for s in sour_matches:
        print(f" -> [{s.code}] {s.name} ({s.category_name})")

    print("\n--- 3. Exemplo de Busca por Palavra-Chave 'trigo' ---")
    wheat_matches = db.search_by_keyword("trigo")
    for s in wheat_matches:
        print(f" -> [{s.code}] {s.name}")


if __name__ == "__main__":
    cli()
