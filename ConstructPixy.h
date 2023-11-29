// Code to create and update the pixy Array struct, average and
// return date to main program/hub

#define CREW 4

// define pre setup signatures in decimal format (from octal)
// define more or less signatures here along with crew size
#define SIG12 10
#define SIG13 11
#define SIG14 12
#define SIG24 28

// change this value based on camera ID
#define ID 4

#define MINFRAMES 40 // 2 times the frames per second expected

struct crewMember // index 0 for right and 1 for left shoulder, if one, all
{
  uint16_t camID = ID;
  uint16_t sig;
  uint16_t height[2];
  uint16_t width[2];
  uint16_t x[2];
  uint16_t y[2];
  int16_t angle[2];
  bool isDetected;
};

struct patchData
{
  uint16_t sig;
  uint16_t height[MINFRAMES];
  uint16_t width[MINFRAMES];
  int16_t angle[MINFRAMES];
  uint16_t x[MINFRAMES];
  uint16_t y[MINFRAMES];
  uint8_t index;
  uint16_t count;
  bool detected;
} patch[CREW];

uint16_t signatures[CREW] = { SIG12, SIG13, SIG14, SIG24};

// fucntions to define and manipulate sig data
class CalculateData
{
  // crewMember cm[CREW]; // array to send crew data to hub
  // uint16_t right_left[MINFRAMES]; // based on shoulder position of patch

public:
  crewMember cm[CREW]; // array to send crew data to hub
  uint16_t right_left[MINFRAMES]; // based on shoulder position of patch
  // constructor for crewMember (cm) array to inizilize sig values
  CalculateData()
  {
    for(uint16_t i = 0; i < CREW; i++)
    {
      cm[i].sig = signatures[i];
      cm[i].height[0] = cm[i].height[1] = 0;
      cm[i].width[0] = cm[i].width[1] = 0;
      cm[i].x[0] = cm[i].x[1] = 0;
      cm[i].y[0] = cm[i].y[1] = 0;
      cm[i].angle[0] = cm[i].angle[1] = 0;
    }
  }
  
  // get the average of the height of the patch
  void getHeight(int curr)
  {
    uint16_t right = 0;
    uint16_t left = 0;
    int i;
    for(i = 0; i < MINFRAMES; i++)
    {
      if(i < MINFRAMES / 2)
      {
        right = right + patch[curr].height[right_left[i]];
      }
      else
      {
        left = left + patch[curr].height[right_left[i]];
      }
    }
    
    cm[curr].height[0] = right / (MINFRAMES / 2);
    cm[curr].height[1] = left / (MINFRAMES / 2);
  }

  // get the average of the width of the patch
  void getWidth(int curr)
  {
    uint16_t right = 0;
    uint16_t left = 0;
    uint16_t i;
    for(i = 0; i < MINFRAMES; i++)
    {
      if(i < MINFRAMES / 2)
      {
        right = right + patch[curr].width[right_left[i]];
      }
      else
      {
        left = left + patch[curr].width[right_left[i]];
      }
    }

    cm[curr].width[0] = right / (MINFRAMES / 2);
    cm[curr].width[1] = left / (MINFRAMES / 2);
  }

  //
  // get the mode of the angle of the patch
  //
  void getAngle(int curr)
  {
    int modeArr[MINFRAMES/2];
    int modeArr2[MINFRAMES/2];
    int count = 0;
    int count2 = 0;
    uint16_t right = 0;
    uint16_t left = 0;
    uint16_t i;
    for(i = 0; i < MINFRAMES; i++)
    {
      if(i < MINFRAMES / 2)
      {
        int x = patch[curr].angle[right_left[i]];
        if(x <= 0) {x = x + 360;}
        modeArr[count] = x;
        count++;
      }
      else
      {
        int x = patch[curr].angle[right_left[i]];
        if(x <= 0) {x = x + 360;}
        modeArr2[count2] = x;
        count2++;
      }
    }

    cm[curr].angle[0] = mode(modeArr, count);
    cm[curr].angle[1] = mode(modeArr2, count2);    
  }

  // get center of between patches by x values
  void getX(uint16_t curr)
  {
    uint16_t right = 0;
    uint16_t left = 0;
    uint16_t i;
    for(i = 0; i < MINFRAMES; i++)
    {
      if(i < MINFRAMES / 2)
      {
        right = right + patch[curr].x[right_left[i]];
      }
      else
      {
        left = left + patch[curr].x[right_left[i]];
      }
    }
    cm[curr].x[0] = right / (MINFRAMES / 2);
    cm[curr].x[1] = left / (MINFRAMES / 2);  
  }

  // get y value from available patch values
  void getY(uint16_t curr)
  {
    int16_t right = 0;
    uint16_t left = 0;
    uint16_t i;
    for(i = 0; i < MINFRAMES; i++)
    {
      if(i < MINFRAMES / 2)
      {
        right = right + patch[curr].y[right_left[i]];
      }
      else
      {
        left = left + patch[curr].y[right_left[i]];
      }
    }
    cm[curr].y[0] = right / (MINFRAMES / 2);
    cm[curr].y[1] = left / (MINFRAMES / 2);  
  }

  // Main data function
  // combine patch data and store in struct array
  void patchToData(uint16_t curr)
  {
    //getHeight(curr);
    //getWidth(curr);
    getX(curr);
    getY(curr);
    getAngle(curr);
    cm[curr].isDetected = patch[curr].detected;
  }

  // compile sort index for left and right patch
  void left_or_right(uint16_t curr)
  {
    bool right = false; 
    // is right patch the even or odd index
    if(patch[curr].x[0] < patch[curr].x[1] && abs(patch[curr].angle[0]) < 90)
    {
      right = true;
    }
    else if(patch[curr].x[0] > patch[curr].x[1] && abs(patch[curr].angle[0]) >= 90)
    {
      right = true;
    }
    
    sortArray(right);
  }

  /*****************************
  *sort left_right index array
  ******************************/
  void sortArray(bool right)
  {
    uint16_t value = 0;
    if(right)
    {
      uint16_t value = 0;
      for(uint16_t i = 0; i < MINFRAMES / 2; i++)
      {
        right_left[i] = value;
        value += 2;
      }
      value = 1;
      for(uint16_t i = MINFRAMES / 2; i < MINFRAMES; i++)
      {
        right_left[i] = value;
        value += 2;
      }
    }
    else
    {
      value = 1;
      for(int16_t i = 0; i < MINFRAMES / 2; i++)
      {
        
        right_left[i] = value;
        value += 2;
      }
      value = 0;
      for(int16_t i = MINFRAMES / 2; i < MINFRAMES; i++)
      {
        
        right_left[i] = value;
        value += 2;
      }
    }
  }

  /*****************************
  *print data
  ******************************/
  void printData()
  {
    for (uint8_t i=0; i<CREW; i++)
    {
      // print crew member data
      if(cm[i].isDetected)
      {
        Serial.print("Block ");
        Serial.println(cm[i].sig);
        // Serial.print("Height Right: ");
        // Serial.println(cm[i].height[0]);
        // Serial.print("Height Left: ");
        // Serial.println(cm[i].height[1]);
        // Serial.print("Width Right: ");
        // Serial.println(cm[i].width[0]);
        // Serial.print("Width Left: ");
        // Serial.println(cm[i].width[1]);
        Serial.print("x right: ");
        Serial.println(cm[i].x[0]);
        Serial.print("x Left: ");
        Serial.println(cm[i].x[1]);
        // Serial.print("y right: ");
        // Serial.println(cm[i].y[0]);
        // Serial.print("y Left: ");
        // Serial.println(cm[i].y[1]);
        // Serial.print("Angle Right: ");
        // Serial.println(cm[i].angle[0]);
        // Serial.print("Angle Left: ");
        // Serial.println(cm[i].angle[1]);
      
        Serial.println("---------------------------");
      }
      
    }
  }

  // for viewing the data from any given patch signature
  void printPatchData(int curr)
  {
    Serial.print("Sig : ");
    Serial.println(patch[curr].sig);
    Serial.print("Patch ");
    for(uint8_t i = 0;i < MINFRAMES;i++)
    {
      
      Serial.print("X ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(patch[curr].x[i]);
    }
  }

  /*************************************************
  * check if signature applies to current application
  **************************************************/
  bool isValidSignature(int sig)
  {
    switch (sig)
    {
      case SIG12:
      case SIG13:
      case SIG14:
      case SIG24:
        return true;
      default:
        return false;
  
    }
  }
  /*****************************
  * reset patch count
  ******************************/
  void resetPatchCount()
  {
    for(uint8_t i=0;i<CREW;i++)
    {
      patch[i].count = 0;
      memset(patch[i].x, 0 , sizeof(patch[i].x));
      memset(patch[i].y, 0 , sizeof(patch[i].y));
      patch[i].detected = false;
      // patch[i].index = -1;
    }
  }

  /********************************************************
  *  calculate mode of a given list of numbers
  *********************************************************/
  int mode(int a[],int n) {
   int maxValue = 0, maxCount = 0, i, j;

   for (i = 0; i < n; ++i) {
      int count = 0;
      
      for (j = 0; j < n; ++j) {
         if (a[j] == a[i])
         ++count;
      }
      
      if (count > maxCount) {
         maxCount = count;
         maxValue = a[i];
      }
   }

   return maxValue;
  }
}; //end class
