<code>
for each row r do begin
	for each hash function h<sub>i</sub> do
		compute h<sub>i</sub>(r)
	for each column c
		if c has 1 in row r:
			for each hash function h<sub>i</sub> do
				if h<sub>i</sub>(r) is smaller than M(i,c) then
					M(i, c) := h<subscript>i</sub>(r)
</code>

M(i, c) = value in column 'c' for 'i'th hash function
