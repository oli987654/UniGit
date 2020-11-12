\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{exercise}[2014/15/11 v0.03]

\LoadClass[a4paper,11pt,oneside,fleqn]{article}

\DeclareOption*{% 
    \PassOptionsToClass{\CurrentOption}{article}% 
}
\ProcessOptions\relax

\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
\RequirePackage{microtype}

\RequirePackage[left=3cm,right=3cm,top=3cm,bottom=3.5cm]{geometry}
\RequirePackage[english]{babel}
\RequirePackage{tikz}
\RequirePackage[fleqn]{amsmath}
\RequirePackage{amssymb}
\RequirePackage{color}
\RequirePackage{mdframed}
\RequirePackage{xspace}
\RequirePackage{enumitem}
\RequirePackage{dsfont}
\RequirePackage{ellipsis}


\usetikzlibrary{arrows,positioning,automata}
\tikzset{
  every initial by arrow/.style={initial text={}},
  every state/.style={semithick},
  accepting by double/.style={double distance=.4mm},
  font=\small,
  >=stealth', %'
  auto
}

\def\ps@myheadings{%
  \let\@oddfoot\@empty\let\@evenfoot\@empty
  \def\@evenhead{\thepage\hfil\slshape\leftmark}%
  \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
  \let\@mkboth\@gobbletwo
  \let\sectionmark\@gobble
  \let\subsectionmark\@gobble
}

\global\let\thanks\relax
\global\let\@thanks\@empty 
\global\let\@author\@empty
\global\let\author\relax
\global\let\date\relax
\global\let\@date\@empty
\global\let\and\relax

\def\@lefttitle{Use \texttt{$\backslash$lefttitle$\{$Text$\}$}}
\def\@righttitle{Use \texttt{$\backslash$righttitle$\{$Text$\}$}}
\def\@title{Use \texttt{$\backslash$title$\{$Text$\}$}}
\def\lefttitle#1{\gdef\@lefttitle{#1}}
\def\righttitle#1{\gdef\@righttitle{#1}}

\renewcommand\maketitle{
  \null
  \hbox to \linewidth{%
    \rlap{\parbox[t]{\linewidth}{%
        \@lefttitle\strut%
    }%
  }\hfill%
  \llap{\parbox[t]{\linewidth}{\raggedleft%
      \@righttitle\strut%
  }}}%
  \vskip 3ex%
  {\parbox[t]{\linewidth}{\centering\LARGE\bfseries \@title}}%
  \vskip0ex%
  \hfill%
  \vskip2ex
}

\newenvironment{taskitems}{%
  \begin{enumerate}[label=\roman*.]%
}{%
  \end{enumerate}%
}

\newenvironment{solution}{%
  \begin{mdframed}[%
    innerlinewidth=0pt,%
    middlelinewidth=0pt,%
    outerlinewidth=3pt,%
    innerlinecolor=white,%
    outerlinecolor=lightgray!30,%
    backgroundcolor=lightgray!30,%
    skipabove=\baselineskip,%
    skipbelow=0pt,%
    userdefinedwidth=\textwidth,%
    innertopmargin=7pt,%
    innerrightmargin=7pt,%
    innerbottommargin=7pt,%
    innerleftmargin=7pt,%
    nobreak=false]%
}{
  \end{mdframed}
}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0.5ex plus 0.1ex minus 0.05ex\relax}
\setlength{\mathindent}{15mm}
\setcounter{secnumdepth}{1}

\pagestyle{empty}

\newcounter{task}
\renewcommand\thetask{\@arabic\c@exercise.\@arabic\c@task\relax}
\let\taskmark\@gobble

\newcommand\task{\par

  \outofsubt@sk%
  \c@subtask=0\@startsection{task}{1}{0ex}%
  {-3.5ex \@plus -1ex \@minus -.2ex}%
  {0.3ex \@plus.2ex}%
  {\normalfont\bfseries}}

\newcounter{exercise}
\newif{\ifinsubt@sk}
\insubt@skfalse

\newcounter{subtask}
\def\getintosubt@sk{
  \ifinsubt@sk\else%
       \global\advance\@listdepth\@ne%
       \global\advance\@enumdepth\@ne%
       \@listi
       \advance\linewidth -\rightmargin
       \advance\linewidth -\leftmargin
       \advance\@totalleftmargin \leftmargin
       \advance\leftskip\leftmargin
  \fi%
  \global\insubt@sktrue%
}

\def\outofsubt@sk{
  \ifinsubt@sk%
       \global\advance\@listdepth\m@ne%
       \global\advance\@enumdepth\m@ne%
       \@listi
       \advance\linewidth\rightmargin
       \advance\linewidth\leftmargin
       \advance\@totalleftmargin-\leftmargin
       \advance\leftskip-\leftmargin
  \fi%
  \global\insubt@skfalse%
}
\newcommand*{\subtask}[1][]{\par\vskip0.5ex plus 0.2ex minus0.1ex%
             \getintosubt@sk%
             \advance\c@subtask by 1%
             {\noindent\llap{{#1}\hskip0.3em\bfseries\@alph\c@subtask)%
                             \hskip0.5em}}}
\def\nosubtask{\par\vskip0.5ex plus 0.2ex minus0.1ex%
               \outofsubt@sk}

\newcommand{\rev}{\ensuremath{\textsf{R}}}
\newcommand{\nat}{\ensuremath{\mathds{N}}\xspace}
\newcommand{\integ}{\ensuremath{\mathds{Z}}\xspace}
\newcommand{\rat}{\ensuremath{\mathds{Q}}\xspace}
\newcommand{\real}{\ensuremath{\mathds{R}}\xspace}
\newcommand{\ie}{that is\xspace}
\newcommand{\eg}{for instance\xspace}
\newcommand{\rmove}{\rightarrow\xspace}
\newcommand{\lmove}{\leftarrow\xspace}
\newcommand{\nomove}{\downarrow\xspace}
\newenvironment{mlabels}{ %
  $\begin{array}{c}%
}{%
  \end{array}$%
}%
\newcommand{\tmlabel}[3]{#1\,/\,#2, #3}
\newcommand{\mtmlabel}[3]{#1\,/\,#2; #3}
\newcommand{\pdalabel}[3]{#1, #2\,/\,#3}

\endinput
