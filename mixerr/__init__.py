"""
Generate representative mixes from the solution space
"""
# Imports
import clingo
import sys
import random
import argparse
import textwrap
import os
import scipy.io
from scipy.io.wavfile import write
from . import utilities as util
from . import table
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal
import xml.etree.ElementTree as ET

## To complement the mixer logic program with python support
from clingo.symbol import Number

""" 
Class context to complement python processing in clingo
"""
class Context:

    def db2linear(self, x):
        linear = int(pow(10, x.number/20) * 100)# int(log10(x.number / 100) * 20)
        return Number(linear)


""" 
Parse results from grid
""" 
def parse_results(model, answer_sets, edges, display):
    table.build(model, answer_sets, edges, display)

    
""" 
Parse Arguments 
"""
def parse_params():
    parser = argparse.ArgumentParser(prog='mixerr.py',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=textwrap.dedent('''\
                                     mixerr. Representative mixes from the solution space.
                                     Default command-line (mixerr and player):
                                     f=Nerve9_PrayForTheRain; python -m mixerr --project=$f && python mixerr/player.py --project=$f
                                     mixerr only command-line: python -m mixerr --project=Nerve9_PrayForTheRain
                                     '''))
    
    ## Input related to uniform solving and sampling
    basic_args = parser.add_argument_group("Basic Options")

    parser.add_argument("--project", type=str, default="Nerve9_PrayForTheRain",
                        help="The running project. Default: Nerve9_PrayForTheRain")
    parser.add_argument('--display', action='store_true',
                        help="Display additional information from the inner processes")

    return parser.parse_args()
    
""" 
Main function

How mixerr works
1) Read all the tracks/stems from the given project
2) Get all the number of tracks and all the symbols from a clingo object
3) Build the XORs to generate 16 clusters
4) For loop... for each XORs configuration
   5) Create a new clingo object
   6) Add the encodings and the XORs
   7) Ground, Solve and store answer set
8) If all SAT, proceed... else restart
9) Create a new clingo object and perform the representative grid search
10) Perform tracks normalization
11) Generate mixes, plans and plots
12) Write the output XML file
* The player is in charge to build the grid and the UI
   13) Build the player
   14) Build the grid
   15) Build the plan area
   16) Build the plots area

"""
def main():

    args = parse_params()

    audio_project   = args.project
    display         = args.display

    tracks = {}
    track_names = {}
    track_id = 1
    ## 1) Read all the tracks/stems from the given project
    project = "mixerr/projects/%s"%audio_project
    audio_files = sorted([f for f in os.listdir(project) if os.path.join(project, f) and f.endswith(".wav")])

    print("Project:", audio_project)
    
    len_track = 0
    for audio in audio_files:
        print("Reading audio file:", audio)
        track_names[track_id] = audio
        sr, x = scipy.io.wavfile.read(os.path.join(project, audio))
        tracks[track_id] = x
        len_track = len(x)
        #print("Length of tracks in samples:", len_track)
        track_id += 1
        
    num_tracks = len(tracks)
    print("Number of tracks:", num_tracks)

    ## Create output directory for the resultant mixes
    path = "mixerr/results/%s"%audio_project
    # Check whether the specified path exists or not
    if not os.path.exists(path):
        # Create a new directory because it does not exist
        print("Creating results directories")
        os.makedirs(path)
        os.makedirs(path+"/mixes")
        os.makedirs(path+"/plans")
        os.makedirs(path+"/plots")

    ## 2) Get all the number of tracks and all the symbols from a clingo object

    ctl = clingo.Control()
    ctl.add("base", [], "#const tracks = %s."%num_tracks)
    ctl.load("mixerr/lp/normalized_db_mixer.lp")
    ctl.load("mixerr/lp/dBFSPerTracks.lp")
    
    ctl.ground([("base", [])], context=Context())

    atoms = [x.symbol for x in ctl.symbolic_atoms.by_signature("track_decibel",2)]
    atoms_per_track = {}
    ## Be sure to pick XORs that do not contradict. For instance, using the same track twice
    ## odd track 1 is -30 and odd that track 1 is -12... this is UNSAT
    for atom in atoms:
        track = int(str(atom.arguments[0]))
        atoms_per_track.setdefault(track, []).append(atom)

    
    ## 3) Build the XORs to generate 16 clusters
    # N XORs
    n = 4
    num_clusters = n * n
    ## Build 2^n combinatios for XOR constraints
    ttable = util.truthtable(n)

    sat_counter = 0

    while sat_counter != num_clusters: ## Run until satisfiability
        print("Generating mixes...")
        answer_sets = []
        random_tracks = random.sample(range(1,num_tracks + 1), n)
        if display:
            ## Random tracks to create XORs
            print(random_tracks)

        random_atoms = []
        for track in random_tracks:
            random_atoms.append(random.sample(atoms_per_track[track], 1)[0])

        if display:
            ## Generated atoms for XORs
            [print(atom) for atom in random_atoms] 

        iteration = 1
        ## 4) For loop... for each XORs configuration
        for line in ttable:

            ## 5) Create a new clingo object
            if display:
                print("Iteration:", iteration)
            ctl = clingo.Control()

            ctl.add("base", [], "#const tracks = %s."%num_tracks)

            ## 6) Add the encodings and the XORs
            ctl.load("mixerr/lp/normalized_db_mixer.lp")
            ctl.load("mixerr/lp/dBFSPerTracks.lp")

            for i in range(len(line)):
                atom   = random_atoms[i]
                parity = line[i]
                xor = ""
                if parity == 1:
                    xor = ":- not %s."%atom
                else:
                    xor = ":- %s."%atom

                ctl.add("base", [], xor)
                if display:
                    print(xor)

            ## 7) Ground, Solve and store answer set
            ## Ground
            if display:
                print("Grounding...")
            ctl.ground([("base", [])], context=Context())
            ## Solve
            if display:
                print("Solving...")
            with ctl.solve(yield_=True) as hnd:
                for m in hnd:
                    if display:
                        print("Answer: %s"%m.number)
                        print(m)
                    atoms_list = m.symbols(shown=True)
                    answer_sets.append(atoms_list)

                if (str(hnd.get()) == "SAT"):
                    if display:
                        print("SATISFIABLE")
                    ## 8) If all SAT, proceed... else restart
                    sat_counter += 1
                elif (str(hnd.get()) == "UNSAT"):
                    if display:
                        print("UNSATISFIABLE")
                    break
                else:
                    if display:
                        print("UNKNOWN")

            ## New interation
            iteration += 1
            if display:
                print()


    if display:
        print(len(answer_sets))
        for answer in answer_sets:
            print(answer)

    ## 9) Create a new clingo object and perform the representative grid search
    ## Calculate edges and build the instance
    size = n
    diagonals = False

    plain_approach = True ## Full eager approach
    instance, edges, min_dist, max_dist = util.build_instance(answer_sets, 1, size, diagonals, plain_approach)

    ## Display the instance for optimization
    if display:
        print(instance)

    ## Perform a k-incremental approach until satisfiable
    sat = False
    k = min_dist
    last_model = []
    while sat is False:
        if display:
            print("checking with distance k:", k)
    
        ctl = clingo.Control()
        #print(ctl.configuration.solve.description("solve_limit"))
        ctl.configuration.solve.solve_limit = 500000
        ctl.add("base", [], instance)
        k_constraint = "#const k=%s.\n"%k
        k_constraint += ":- distance(A1,A2,D), cluster(X,A1), cluster(Y,A2), edge(X,Y), X<Y, D>k."
        ctl.add("base", [], k_constraint)

        ctl.load("mixerr/lp/representative.lp")
        if display:
            print("Grounding...")
        ctl.ground([("base", [])])

        ## Solve
        if display:
            print("Solving...")
        with ctl.solve(yield_=True) as hnd:
            for m in hnd:
                last_model = []
                parse_results(m, answer_sets, edges, display)
                atoms_list = m.symbols(shown=True)
                last_model.append(atoms_list)
            if (str(hnd.get()) == "SAT"):
                if display:
                    print("SATISFIABLE")
                sat = True
            elif (str(hnd.get()) == "UNSAT"):
                if display:
                    print("UNSATISFIABLE")
                k += 1
            else:
                if display:
                    print("UNKNOWN")
                k += 1

    ## The (optimum) model
    print("Optimum model found!")
    grid_list = []

    for model in last_model:
        if display:
            print(model)
        for i in range(1, num_clusters+1):
            for atom in model:
                if "cluster" in atom.name:
                    cell       = int(str(atom.arguments[0]))
                    answer_set = int(str(atom.arguments[1]))
                    if i == cell:
                        grid_list.append(answer_set)
                        if display:
                            print("cell:", cell, "answer:", answer_set)
        
    ## 10) Perform tracks normalization and mono output processing
    print("Normalizing tracks...") 
    #for tid, track in tracks.items():
    #    #num_channels = len(track[0])
    #    print("Processing track:", tid)#, "num channels", num_channels)
    #    num_samples = len(track)

        ## Mono
        #if num_channels == 1:

    #    peak = np.max(np.abs(track))
    #    track = np.array([track / peak * 32767], np.int16)

    #    print(np.shape(track), np.shape(tracks[tid]))
    #    tracks[tid] = track[0]
            
            #max_left  = 0
            #for i in range(num_samples):
            #    amp = 
            #    if abs(amp) > max_left:
            #        max_left = abs(amp)

            #for i in range(num_samples):
            #    track[:, 0][i] /= max_left

        ## Stereo
        #elif num_channels == 2:

        #    peakl = np.max(np.abs(track[:, 0]))
        #    peakr = np.max(np.abs(track[:, 1]))
        #    peak = max(peakl, peakr)
        #    track[:, 0] = np.array([track[:, 0] / peak * 32767], np.int16)
        #    track[:, 1] = np.array([track[:, 1] / peak * 32767], np.int16)

            #track = track[:, 0] + track[:, 1]
            
            #max_left  = 0
            #max_right = 0
            #for i in range(num_samples):
            #    ampl = track[:, 0][i]
            #    ampr = track[:, 1][i]
            #    if abs(ampl) > max_left:
            #        max_left  = abs(ampl)
            #    if abs(ampr) > max_right:
            #        max_right = abs(ampr)

            #for i in range(num_samples):
            #    track[:, 0][i] /= max_left
            #    track[:, 1][i] /= max_right

        ## Immersive formats... not supported for now
        #else:
        #    print("Number of channels not supported")

    ## 11 Generate mixes, plans and plots
    track_id  = 0
    track_db  = 1
    model = 1
    for answer in answer_sets:
        print("Parsing answer %s to wav, plan and plots"%model)
        
        if display:
            print("Answer:", model)
        mix = np.zeros(len_track)
        total_gain = 0

        if display:
            print("Writing answer to file")
        filename = "mixerr/results/%s/plans/Mix_Answer %s.txt"%(audio_project, model)
        output = ""
        
        for atom in sorted(answer):
            if display:
                print(atom)
            track = int(str(atom.arguments[track_id]))
            db    = int(str(atom.arguments[track_db]))
            gain  = util.dBFS2Gain(db)
            total_gain += gain
            
            output += "  Track: %s %s dBFS\n"%(track_names[track], db)              
            current_track = np.copy(tracks[track])
            mix += current_track * gain

        with open(filename, 'w') as f:
            if display:
                print(output)
            f.write(output+"\n")
            
        f.close()
        if display:
            print("Peak dBFS:", util.gain2dBFS(total_gain))
            print()

        if display:
            print("Rendering wav file")
        filename = "mixerr/results/%s/mixes/Mix_Answer %s.wav"%(audio_project, model)
        ## Check the sample rate from the project

        ## Check export not rendering in the desired range
        ## Normalize the output?
        write(filename, 44100, mix.astype(np.int16))

        spectre = np.fft.fft(mix)
        freq = np.fft.fftfreq(mix.size, 1/44100)
        mask=freq>0

        frequencies, times, spectrogram = signal.spectrogram(mix, 44100)

        if display:
            print("Generating plots")
        ## Plot
        plt.figure(figsize=(12,7))
        plt.subplot(211)
        plt.grid(True)
        plt.plot(mix)
        plt.title("Time domain")
        plt.xlabel('Time (s)')
        plt.ylabel('Linear Amp [0-1]')

        plt.subplot(212)
        plt.grid(True)
        plt.plot(freq[mask],np.abs(spectre[mask]))
        plt.title(" Spectrum")
        plt.xlabel('Frequency')
        plt.xlim(xmin=20)
        plt.ylabel('Linear Amp [0-1]')
        plt.xscale('log')

        plt.tight_layout()

        plotfile = "mixerr/results/%s/plots/Mix_Answer %s.png"%(audio_project, model)
        plt.savefig(plotfile)
        #if args.show_plot:
        #    plt.show()

        model += 1

    ## 12) Writing the generated XML file
    ## Pass this to the utility file
    print("Writing the output XML file")
    ## This is the parent (root) tag onto which other tags would be created
    data = ET.Element('mixerr')

    ## Adding a subtag named `project` inside our root tag
    project_element = ET.SubElement(data, 'project')
    ## Set the project name
    project_element.set('name', '%s'%audio_project)

    ## Adding a subtag named `grid` inside our root tag
    grid_element = ET.SubElement(data, 'grid')

    answer = 1
    for element in grid_list:
        grid_elem1 = ET.SubElement(grid_element, 'answer') 
        grid_elem1.set('number', '%s'%answer)

        ## Adding text between the `answer` subtag
        grid_elem1.text = "%s"%element
        answer += 1

    ## Converting the xml data to byte object, for allowing flushing data to file stream
    b_xml = ET.tostring(data)

    ## Opening a file under the name `results.xml`,
    ## with operation mode `wb` (write + binary)
    xml_path = path + "/%s.xml"%(audio_project)
    with open(xml_path, "wb") as f:
        f.write(b_xml)
    
                
"""
Main function
"""
if __name__ == '__main__':
    sys.exit(main())
