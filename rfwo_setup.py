# Continuous Integration

def setup(indata,minyear,maxyear,minrating,maxrating,minratingLetterboxd,maxratingLetterboxd,minpopularity,maxpopularity,genre,number,director,actor):
	indata = indata.replace('minyear = 0','minyear = '+str(minyear))
	indata = indata.replace('maxyear = 0','maxyear = '+str(maxyear))
	indata = indata.replace('minrating = 0','minrating = '+str(minrating))
	indata = indata.replace('maxrating = 0','maxrating = '+str(maxrating))
	indata = indata.replace('minratingLetterboxd = 0','minratingLetterboxd = '+str(minratingLetterboxd))
	indata = indata.replace('maxratingLetterboxd = 0','maxratingLetterboxd = '+str(maxratingLetterboxd))
	indata = indata.replace('minpopularity = 0','minpopularity = '+str(minpopularity))
	indata = indata.replace('maxpopularity = 0','maxpopularity = '+str(maxpopularity))
	indata = indata.replace('genre = any','genre = '+genre)
	indata = indata.replace('number = 1','number = '+str(number))
	indata = indata.replace('director = none','director = '+director)
	indata = indata.replace('actor = none','actor = '+actor)
	return indata

# Read in input file:
infile = open("rfwo_input.txt","r")
indata = infile.read()

# Get output files ready:
outfile1  = open("CI/input1.txt", "w")
outfile2  = open("CI/input2.txt", "w")
outfile3  = open("CI/input3.txt", "w")
outfile4  = open("CI/input4.txt", "w")
outfile5  = open("CI/input5.txt", "w")
outfile6  = open("CI/input6.txt", "w")
outfile7  = open("CI/input7.txt", "w")
outfile8  = open("CI/input8.txt", "w")
outfile9  = open("CI/input9.txt", "w")
outfile10 = open("CI/input10.txt","w")
outfile11 = open("CI/input11.txt","w")
outfile12 = open("CI/input12.txt","w")
outfile13 = open("CI/input13.txt","w")
outfile14 = open("CI/input14.txt","w")
outfile15 = open("CI/input15.txt","w")
outfile16 = open("CI/input16.txt","w")
outfile17 = open("CI/input17.txt","w")
outfile18 = open("CI/input18.txt","w")
outfile19 = open("CI/input19.txt","w")
outfile20 = open("CI/input20.txt","w")

indata1  = setup(indata,0,   0,   0,0,0,0,0,0,'any',1,'none','none')
indata2  = setup(indata,1970,0,   0,0,0,0,0,0,'any',1,'none','none')
indata3  = setup(indata,0,   1980,0,0,0,0,0,0,'any',1,'none','none')
indata4  = setup(indata,1970,1980,0,0,0,0,0,0,'any',1,'none','none')

indata5  = setup(indata,0,0,3.0,0,  0,0,0,0,'any',1,'none','none')
indata6  = setup(indata,0,0,0,  4.0,0,0,0,0,'any',1,'none','none')
indata7  = setup(indata,0,0,3.0,4.0,0,0,0,0,'any',1,'none','none')

indata8  = setup(indata,0,0,0,0,3.0,  0,0,0,'any',1,'none','none')
indata9  = setup(indata,0,0,0,0,0,  4.0,0,0,'any',1,'none','none')
indata10 = setup(indata,0,0,0,0,3.0,4.0,0,0,'any',1,'none','none')

indata11 = setup(indata,0,0,0,0,0,0,40.0,0,   'any',1,'none','none')
indata12 = setup(indata,0,0,0,0,0,0,0,   50.0,'any',1,'none','none')
indata13 = setup(indata,0,0,0,0,0,0,40.0,50.0,'any',1,'none','none')

indata14 = setup(indata,0,0,0,0,0,0,0,0,'horror', 1,'none','none')
indata15 = setup(indata,0,0,0,0,0,0,0,0,'romcom', 1,'none','none')
indata16 = setup(indata,0,0,0,0,0,0,0,0,'romdram',1,'none','none')
indata17 = setup(indata,0,0,0,0,0,0,0,0,'actadv', 1,'none','none')

indata18 = setup(indata,0,0,0,0,0,0,0,0,'any',5,'none','none')

indata19 = setup(indata,0,0,0,0,0,0,0,0,'any',1,'quentin-tarantino','none')

indata20 = setup(indata,0,0,0,0,0,0,0,0,'any',1,'none','brad-pitt')

outfile1.write(indata1)
outfile2.write(indata2)
outfile3.write(indata3)
outfile4.write(indata4)
outfile5.write(indata5)
outfile6.write(indata6)
outfile7.write(indata7)
outfile8.write(indata8)
outfile9.write(indata9)
outfile10.write(indata10)
outfile11.write(indata11)
outfile12.write(indata12)
outfile13.write(indata13)
outfile14.write(indata14)
outfile15.write(indata15)
outfile16.write(indata16)
outfile17.write(indata17)
outfile18.write(indata18)
outfile19.write(indata19)
outfile20.write(indata20)

infile.close()
outfile1.close()
outfile2.close()
outfile3.close()
outfile4.close()
outfile5.close()
outfile6.close()
outfile7.close()
outfile8.close()
outfile9.close()
outfile10.close()
outfile11.close()
outfile12.close()
outfile13.close()
outfile14.close()
outfile15.close()
outfile16.close()
outfile17.close()
outfile18.close()
outfile19.close()
outfile20.close()
