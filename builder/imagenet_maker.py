
import logging

logging.basicConfig(filename='imagenet_maker_.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('Setting up logger')


import time
import requests
import pathlib
from collections import defaultdict
from tqdm.auto import tqdm

inet_name_mapper = defaultdict()

# Get the human readable identifications ... Walker hound for instance
sysnet_word_prefix = 'http://www.image-net.org/api/text/wordnet.synset.getwords?wnid={WORDNET_ID}'

# Gets the urls
image_url_prefix = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={WORDNET_ID}'

wordnet_ids = [
    "n02119789", "n02100735", "n02110185", "n02096294", "n02102040", "n02066245", "n02509815",
    "n02124075", "n02417914", "n02123394", "n02125311", "n02423022", "n02346627", "n02077923",
    "n02110063", "n02447366", "n02109047", "n02089867", "n02102177", "n02091134", "n02092002",
    "n02071294", "n02442845", "n02504458", "n02092339", "n02098105", "n02096437", "n02114712",
    "n02105641", "n02128925", "n02091635", "n02088466", "n02096051", "n02117135", "n02138441",
    "n02493509", "n02457408", "n02389026", "n02443484", "n02110341", "n02089078", "n02086910",
    "n02097130", "n02445715", "n02093256", "n02113978", "n02106382", "n02441942", "n02113712",
    "n02113186", "n02105162", "n02415577", "n02356798", "n02488702", "n02123159", "n02098413",
    "n02422699", "n02114855", "n02094433", "n02111277", "n02132136", "n02119022", "n02091467",
    "n02106550", "n02422106", "n02091831", "n02120505", "n02104365", "n02086079", "n02112706",
    "n02098286", "n02095889", "n02484975", "n02137549", "n02500267", "n02129604", "n02090721",
    "n02396427", "n02108000", "n02391049", "n02412080", "n02108915", "n02480495", "n02110806",
    "n02128385", "n02107683", "n02085936", "n02094114", "n02087046", "n02100583", "n02096177",
    "n02494079", "n02105056", "n02101556", "n02123597", "n02481823", "n02105505", "n02088094",
    "n02085782", "n02489166", "n02364673", "n02114548", "n02134084", "n02480855", "n02090622",
    "n02113624", "n02093859", "n02403003", "n02097298", "n02108551", "n02493793", "n02107142",
    "n02096585", "n02107574", "n02107908", "n02086240", "n02102973", "n02112018", "n02093647",
    "n02397096", "n02437312", "n02483708", "n02097047", "n02106030", "n02099601", "n02093991",
    "n02110627", "n02106166", "n02326432", "n02108089", "n02097658", "n02088364", "n02111129",
    "n02100236", "n02486261", "n02115913", "n02486410", "n02487347", "n02099849", "n02108422",
    "n02104029", "n02492035", "n02110958", "n02099429", "n02094258", "n02099267", "n02395406",
    "n02112350", "n02109961", "n02101388", "n02113799", "n02095570", "n02128757", "n02101006",
    "n02115641", "n02097209", "n02342885", "n02097474", "n02120079", "n02095314", "n02088238",
    "n02408429", "n02133161", "n02328150", "n02410509", "n02492660", "n02398521", "n02112137",
    "n02510455", "n02093428", "n02105855", "n02111500", "n02085620", "n02123045", "n02490219",
    "n02099712", "n02109525", "n02454379", "n02111889", "n02088632", "n02090379", "n02443114",
    "n02361337", "n02105412", "n02483362", "n02437616", "n02107312", "n02325366", "n02091032",
    "n02129165", "n02102318", "n02100877", "n02074367", "n02504013", "n02363005", "n02102480",
    "n02113023", "n02086646", "n02497673", "n02087394", "n02127052", "n02116738", "n02488291",
    "n02091244", "n02114367", "n02130308", "n02089973", "n02105251", "n02134418", "n02093754",
    "n02106662", "n02444819", "n01882714", "n01871265", "n01872401", "n01877812", "n01873310",
    "n01883070", "n04086273", "n04507155", "n04147183", "n04254680", "n02672831", "n02219486",
    "n02317335", "n01968897", "n03452741", "n03642806", "n07745940", "n02690373", "n04552348",
    "n02692877", "n02782093", "n04266014", "n03344393", "n03447447", "n04273569", "n03662601",
    "n02951358", "n04612504", "n02981792", "n04483307", "n03095699", "n03673027", "n03947888",
    "n02687172", "n04347754", "n04606251", "n03478589", "n04389033", "n03773504", "n02860847",
    "n03218198", "n02835271", "n03792782", "n03393912", "n03895866", "n02797295", "n04204347",
    "n03791053", "n03384352", "n03272562", "n04310018", "n02704792", "n02701002", "n02814533",
    "n02930766", "n03100240", "n03594945", "n03670208", "n03770679", "n03777568", "n04037443",
    "n04285008", "n03444034", "n03445924", "n03785016", "n04252225", "n03345487", "n03417042",
    "n03930630", "n04461696", "n04467665", "n03796401", "n03977966", "n04065272", "n04335435",
    "n04252077", "n04465501", "n03776460", "n04482393", "n04509417", "n03538406", "n03599486",
    "n03868242", "n02804414", "n03125729", "n03131574", "n03388549", "n02870880", "n03018349",
    "n03742115", "n03016953", "n04380533", "n03337140", "n03891251", "n02791124", "n04429376",
    "n03376595", "n04099969", "n04344873", "n04447861", "n03179701", "n03982430", "n03201208",
    "n03290653", "n04550184", "n07742313", "n07747607", "n07749582", "n07753113", "n07753275",
    "n07753592", "n07754684", "n07760859", "n07768694", "n12267677", "n12620546", "n13133613",
    "n11879895", "n12144580", "n12768682", "n03854065", "n04515003", "n03017168", "n03249569",
    "n03447721", "n03720891", "n03721384", "n04311174", "n02787622", "n02992211", "n04536866",
    "n03495258", "n02676566", "n03272010", "n03110669", "n03394916", "n04487394", "n03494278",
    "n03840681", "n03884397", "n02804610", "n03838899", "n04141076", "n03372029", "n11939491",
    "n12057211", "n09246464", "n09468604", "n09193705", "n09472597", "n09399592", "n09421951",
    "n09256479", "n09332890", "n09428293", "n09288635", "n03498962", "n03041632", "n03658185",
    "n03954731", "n03995372", "n03649909", "n03481172", "n03109150", "n02951585", "n03970156",
    "n04154565", "n04208210", "n03967562", "n03000684", "n01514668", "n01514859", "n01518878",
    "n01530575", "n01531178", "n01532829", "n01534433", "n01537544", "n01558993", "n01560419",
    "n01580077", "n01582220", "n01592084", "n01601694", "n01608432", "n01614925", "n01616318",
    "n01622779", "n01795545", "n01796340", "n01797886", "n01798484", "n01806143", "n01806567",
    "n01807496", "n01817953", "n01818515", "n01819313", "n01820546", "n01824575", "n01828970",
    "n01829413", "n01833805", "n01843065", "n01843383", "n01847000", "n01855032", "n01855672",
    "n01860187", "n02002556", "n02002724", "n02006656", "n02007558", "n02009912", "n02009229",
    "n02011460", "n02012849", "n02013706", "n02018207", "n02018795", "n02025239", "n02027492",
    "n02028035", "n02033041", "n02037110", "n02017213", "n02051845", "n02056570", "n02058221",
    "n01484850", "n01491361", "n01494475", "n01496331", "n01498041", "n02514041", "n02536864",
    "n01440764", "n01443537", "n02526121", "n02606052", "n02607072", "n02643566", "n02655020",
    "n02640242", "n02641379", "n01664065", "n01665541", "n01667114", "n01667778", "n01669191",
    "n01675722", "n01677366", "n01682714", "n01685808", "n01687978", "n01688243", "n01689811",
    "n01692333", "n01693334", "n01694178", "n01695060", "n01704323", "n01697457", "n01698640",
    "n01728572", "n01728920", "n01729322", "n01729977", "n01734418", "n01735189", "n01737021",
    "n01739381", "n01740131", "n01742172", "n01744401", "n01748264", "n01749939", "n01751748",
    "n01753488", "n01755581", "n01756291", "n01629819", "n01630670", "n01631663", "n01632458",
    "n01632777", "n01641577", "n01644373", "n01644900", "n04579432", "n04592741", "n03876231",
    "n03483316", "n03868863", "n04251144", "n03691459", "n03759954", "n04152593", "n03793489",
    "n03271574", "n03843555", "n04332243", "n04265275", "n04330267", "n03467068", "n02794156",
    "n04118776", "n03841143", "n04141975", "n02708093", "n03196217", "n04548280", "n03544143",
    "n04355338", "n03891332", "n04328186", "n03197337", "n04317175", "n04376876", "n03706229",
    "n02841315", "n04009552", "n04356056", "n03692522", "n04044716", "n02879718", "n02950826",
    "n02749479", "n04090263", "n04008634", "n03085013", "n04505470", "n03126707", "n03666591",
    "n02666196", "n02977058", "n04238763", "n03180011", "n03485407", "n03832673", "n06359193",
    "n03496892", "n04428191", "n04004767", "n04243546", "n04525305", "n04179913", "n03602883",
    "n04372370", "n03532672", "n02974003", "n03874293", "n03944341", "n03992509", "n03425413",
    "n02966193", "n04371774", "n04067472", "n04040759", "n04019541", "n03492542", "n04355933",
    "n03929660", "n02965783", "n04258138", "n04074963", "n03208938", "n02910353", "n03476684",
    "n03627232", "n03075370", "n03874599", "n03804744", "n04127249", "n04153751", "n03803284",
    "n04162706", "n04228054", "n02948072", "n03590841", "n04286575", "n04456115", "n03814639",
    "n03933933", "n04485082", "n03733131", "n03794056", "n04275548", "n01768244", "n01770081",
    "n01770393", "n01773157", "n01773549", "n01773797", "n01774384", "n01774750", "n01775062",
    "n01776313", "n01784675", "n01990800", "n01978287", "n01978455", "n01980166", "n01981276",
    "n01983481", "n01984695", "n01985128", "n01986214", "n02165105", "n02165456", "n02167151",
    "n02168699", "n02169497", "n02172182", "n02174001", "n02177972", "n02190166", "n02206856",
    "n02226429", "n02229544", "n02231487", "n02233338", "n02236044", "n02256656", "n02259212",
    "n02264363", "n02268443", "n02268853", "n02276258", "n02277742", "n02279972", "n02280649",
    "n02281406", "n02281787", "n01910747", "n01914609", "n01917289", "n01924916", "n01930112",
    "n01943899", "n01944390", "n01945685", "n01950731", "n01955084", "n02319095", "n02321529",
    "n03584829", "n03297495", "n03761084", "n03259280", "n04111531", "n04442312", "n04542943",
    "n04517823", "n03207941", "n04070727", "n04554684", "n03133878", "n03400231", "n04596742",
    "n02939185", "n03063689", "n04398044", "n04270147", "n02699494", "n04486054", "n03899768",
    "n04311004", "n04366367", "n04532670", "n02793495", "n03457902", "n03877845", "n03781244",
    "n03661043", "n02727426", "n02859443", "n03028079", "n03788195", "n04346328", "n03956157",
    "n04081281", "n03032252", "n03529860", "n03697007", "n03065424", "n03837869", "n04458633",
    "n02980441", "n04005630", "n03461385", "n02776631", "n02791270", "n02871525", "n02927161",
    "n03089624", "n04200800", "n04443257", "n04462240", "n03388043", "n03042490", "n04613696",
    "n03216828", "n02892201", "n03743016", "n02788148", "n02894605", "n03160309", "n03000134",
    "n03930313", "n04604644", "n04326547", "n03459775", "n04239074", "n04501370", "n03792972",
    "n04149813", "n03530642", "n03961711", "n03903868", "n02814860", "n07711569", "n07720875",
    "n07714571", "n07714990", "n07715103", "n07716358", "n07716906", "n07717410", "n07717556",
    "n07718472", "n07718747", "n07730033", "n07734744", "n04209239", "n03594734", "n02971356",
    "n03485794", "n04133789", "n02747177", "n04125021", "n07579787", "n03814906", "n03134739",
    "n03404251", "n04423845", "n03877472", "n04120489", "n03062245", "n03014705", "n03717622",
    "n03777754", "n04493381", "n04476259", "n02777292", "n07693725", "n03998194", "n03617480",
    "n07590611", "n04579145", "n03623198", "n07248320", "n04277352", "n04229816", "n02823428",
    "n03127747", "n02877765", "n04435653", "n03724870", "n03710637", "n03920288", "n03379051",
    "n02807133", "n04399382", "n03527444", "n03983396", "n03924679", "n04532106", "n06785654",
    "n03445777", "n07613480", "n04350905", "n04562935", "n03325584", "n03045698", "n07892512",
    "n03250847", "n04192698", "n03026506", "n03534580", "n07565083", "n04296562", "n02869837",
    "n07871810", "n02799071", "n03314780", "n04141327", "n04357314", "n02823750", "n13052670",
    "n07583066", "n03637318", "n04599235", "n07802026", "n02883205", "n03709823", "n04560804",
    "n02909870", "n03207743", "n04263257", "n07932039", "n03786901", "n04479046", "n03873416",
    "n02999410", "n04367480", "n03775546", "n07875152", "n04591713", "n04201297", "n02916936",
    "n03240683", "n02840245", "n02963159", "n04370456", "n03991062", "n02843684", "n03482405",
    "n03942813", "n03908618", "n03902125", "n07584110", "n02730930", "n04023962", "n02769748",
    "n10148035", "n02817516", "n03908714", "n02906734", "n03788365", "n02667093", "n03787032",
    "n03980874", "n03141823", "n03976467", "n04264628", "n07930864", "n04039381", "n06874185",
    "n04033901", "n04041544", "n07860988", "n03146219", "n03763968", "n03676483", "n04209133",
    "n03782006", "n03857828", "n03775071", "n02892767", "n07684084", "n04522168", "n03764736",
    "n04118538", "n03887697", "n13044778", "n03291819", "n03770439", "n03124170", "n04487081",
    "n03916031", "n02808440", "n07697537", "n12985857", "n02917067", "n03938244", "n15075141",
    "n02978881", "n02966687", "n03633091", "n13040303", "n03690938", "n03476991", "n02669723",
    "n03220513", "n03127925", "n04584207", "n07880968", "n03937543", "n03000247", "n04418357",
    "n04590129", "n02795169", "n04553703", "n02783161", "n02802426", "n02808304", "n03124043",
    "n03450230", "n04589890", "n12998815", "n02992529", "n03825788", "n02790996", "n03710193",
    "n03630383", "n03347037", "n03769881", "n03871628", "n03733281", "n03976657", "n03535780",
    "n04259630", "n03929855", "n04049303", "n04548362", "n02979186", "n06596364", "n03935335",
    "n06794110", "n02825657", "n03388183", "n04591157", "n04540053", "n03866082", "n04136333",
    "n04026417", "n02865351", "n02834397", "n03888257", "n04235860", "n04404412", "n04371430",
    "n03733805", "n07920052", "n07873807", "n02895154", "n04204238", "n04597913", "n04131690",
    "n07836838", "n09835506", "n03443371", "n13037406", "n04336792", "n04557648", "n03187595",
    "n04254120", "n03595614", "n04146614", "n03598930", "n03958227", "n04069434", "n03188531",
    "n02786058", "n07615774", "n04525038", "n04409515", "n03424325", "n03223299", "n03680355",
    "n07614500", "n07695742", "n04033995", "n03710721", "n04392985", "n03047690", "n03584254",
    "n13054560", "n10565667", "n03950228", "n03729826", "n02837789", "n04254777", "n02988304",
    "n03657121", "n04417672", "n04523525", "n02815834", "n09229709", "n07697313", "n03888605",
    "n03355925", "n03063599", "n04116512", "n04325704", "n07831146", "n03255030"]


num_train = 10
num_test = 2
dl_path = pathlib.Path("./BABY_IMAGENET")

TOT_IMAGES = 0
REQUEST_ERROR = 0
ALREADY_EXIST = 0
progbar_dict = {}
progbar = tqdm(wordnet_ids)

for wordnet_id in progbar:
    i = 0

    progbar.set_postfix(progbar_dict)
    dl_paths = {
        'train': dl_path / 'train' / wordnet_id,
        'test': dl_path / 'test' / wordnet_id
    }

    for p in dl_paths.values():
        p.mkdir(parents = True, exist_ok = True)
        num_present = len(list(p.glob("*.jpg")))
        i += num_present
        progbar_dict.update({ 'Already Downloaded': str(ALREADY_EXIST := ALREADY_EXIST + num_present) })

    if i >= num_train + num_test:
        continue

    time.sleep(0.5) # we are mking web requests  ... dont be an a-hole
    dl_urls = requests.get(image_url_prefix.format(WORDNET_ID = wordnet_id)).text

    # The bulk of images are .jpg, so it is ok to neglect other formats.
    # It also helps handling urls that dont end in the file format
    # Removing the entries with less than 10 character also removes empty lines and such.
    dl_urls = [ x for x in dl_urls.split("\r\n") if len(x) > 10 and x.endswith(".jpg") ]

    for url in dl_urls:
        progbar.set_postfix(progbar_dict)
        url = pathlib.Path(url)

        if i < num_train:
            subset = "train"
        elif i < num_train + num_test:
            subset = "test"
        else:
            break

        local_path = dl_paths[subset] / url.name

        if not local_path.exists():
            try:
                time.sleep(0.1)
                image_content = requests.get(
                    str(url).replace(":/", "://"),
                    timeout=1)
            except requests.exceptions.ConnectionError as e:
                progbar_dict.update({ 'Request Errors': str(REQUEST_ERROR := REQUEST_ERROR + 1) })
                logging.warning(str(e)+str(url))
                continue
            except requests.exceptions.ReadTimeout as e:
                progbar_dict.update({ 'Request Errors': str(REQUEST_ERROR := REQUEST_ERROR + 1) })
                logging.warning(str(e)+str(url))
                continue
            except requests.exceptions.TooManyRedirects as e: 
                progbar_dict.update({ 'Request Errors': str(REQUEST_ERROR := REQUEST_ERROR + 1) })
                logging.warning(str(e)+str(url))
                continue
            except requests.exceptions.InvalidURL as e: 
                progbar_dict.update({ 'Request Errors': str(REQUEST_ERROR := REQUEST_ERROR + 1) })
                logging.warning(str(e)+str(url))
                continue

            if image_content.ok:
                logging.info(f"Wrote {str(local_path)}")
                open(str(local_path), 'wb').write(image_content.content)
                progbar_dict.update({ 'Downloaded images': str(TOT_IMAGES := TOT_IMAGES + 1) })

                i += 1
            else:
                # print("Skipped a file due to bad request")
                # print(url)
                progbar_dict.update({ 'Request Errors': str(REQUEST_ERROR := REQUEST_ERROR + 1) })
                continue
        else:
            i += 1
            progbar_dict.update({ 'Already Downloaded': str(ALREADY_EXIST := ALREADY_EXIST + 1) })
