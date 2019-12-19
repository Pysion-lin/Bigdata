// ORM class for table 'user_profile'
// WARNING: This class is AUTO-GENERATED. Modify at your own risk.
//
// Debug information:
// Generated date: Sat Sep 07 16:13:27 CST 2019
// For connector: org.apache.sqoop.manager.MySQLManager
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.lib.db.DBWritable;
import com.cloudera.sqoop.lib.JdbcWritableBridge;
import com.cloudera.sqoop.lib.DelimiterSet;
import com.cloudera.sqoop.lib.FieldFormatter;
import com.cloudera.sqoop.lib.RecordParser;
import com.cloudera.sqoop.lib.BooleanParser;
import com.cloudera.sqoop.lib.BlobRef;
import com.cloudera.sqoop.lib.ClobRef;
import com.cloudera.sqoop.lib.LargeObjectLoader;
import com.cloudera.sqoop.lib.SqoopRecord;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class user_profile extends SqoopRecord  implements DBWritable, Writable {
  private final int PROTOCOL_VERSION = 3;
  public int getClassFormatVersion() { return PROTOCOL_VERSION; }
  public static interface FieldSetterCommand {    void setField(Object value);  }  protected ResultSet __cur_result_set;
  private Map<String, FieldSetterCommand> setters = new HashMap<String, FieldSetterCommand>();
  private void init0() {
    setters.put("user_id", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.user_id = (Long)value;
      }
    });
    setters.put("gender", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.gender = (Boolean)value;
      }
    });
    setters.put("birthday", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.birthday = (java.sql.Date)value;
      }
    });
    setters.put("real_name", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.real_name = (String)value;
      }
    });
    setters.put("create_time", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.create_time = (java.sql.Timestamp)value;
      }
    });
    setters.put("update_time", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.update_time = (java.sql.Timestamp)value;
      }
    });
    setters.put("register_media_time", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.register_media_time = (java.sql.Timestamp)value;
      }
    });
    setters.put("id_number", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.id_number = (String)value;
      }
    });
    setters.put("id_card_front", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.id_card_front = (String)value;
      }
    });
    setters.put("id_card_back", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.id_card_back = (String)value;
      }
    });
    setters.put("id_card_handheld", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.id_card_handheld = (String)value;
      }
    });
    setters.put("area", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.area = (String)value;
      }
    });
    setters.put("company", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.company = (String)value;
      }
    });
    setters.put("career", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        user_profile.this.career = (String)value;
      }
    });
  }
  public user_profile() {
    init0();
  }
  private Long user_id;
  public Long get_user_id() {
    return user_id;
  }
  public void set_user_id(Long user_id) {
    this.user_id = user_id;
  }
  public user_profile with_user_id(Long user_id) {
    this.user_id = user_id;
    return this;
  }
  private Boolean gender;
  public Boolean get_gender() {
    return gender;
  }
  public void set_gender(Boolean gender) {
    this.gender = gender;
  }
  public user_profile with_gender(Boolean gender) {
    this.gender = gender;
    return this;
  }
  private java.sql.Date birthday;
  public java.sql.Date get_birthday() {
    return birthday;
  }
  public void set_birthday(java.sql.Date birthday) {
    this.birthday = birthday;
  }
  public user_profile with_birthday(java.sql.Date birthday) {
    this.birthday = birthday;
    return this;
  }
  private String real_name;
  public String get_real_name() {
    return real_name;
  }
  public void set_real_name(String real_name) {
    this.real_name = real_name;
  }
  public user_profile with_real_name(String real_name) {
    this.real_name = real_name;
    return this;
  }
  private java.sql.Timestamp create_time;
  public java.sql.Timestamp get_create_time() {
    return create_time;
  }
  public void set_create_time(java.sql.Timestamp create_time) {
    this.create_time = create_time;
  }
  public user_profile with_create_time(java.sql.Timestamp create_time) {
    this.create_time = create_time;
    return this;
  }
  private java.sql.Timestamp update_time;
  public java.sql.Timestamp get_update_time() {
    return update_time;
  }
  public void set_update_time(java.sql.Timestamp update_time) {
    this.update_time = update_time;
  }
  public user_profile with_update_time(java.sql.Timestamp update_time) {
    this.update_time = update_time;
    return this;
  }
  private java.sql.Timestamp register_media_time;
  public java.sql.Timestamp get_register_media_time() {
    return register_media_time;
  }
  public void set_register_media_time(java.sql.Timestamp register_media_time) {
    this.register_media_time = register_media_time;
  }
  public user_profile with_register_media_time(java.sql.Timestamp register_media_time) {
    this.register_media_time = register_media_time;
    return this;
  }
  private String id_number;
  public String get_id_number() {
    return id_number;
  }
  public void set_id_number(String id_number) {
    this.id_number = id_number;
  }
  public user_profile with_id_number(String id_number) {
    this.id_number = id_number;
    return this;
  }
  private String id_card_front;
  public String get_id_card_front() {
    return id_card_front;
  }
  public void set_id_card_front(String id_card_front) {
    this.id_card_front = id_card_front;
  }
  public user_profile with_id_card_front(String id_card_front) {
    this.id_card_front = id_card_front;
    return this;
  }
  private String id_card_back;
  public String get_id_card_back() {
    return id_card_back;
  }
  public void set_id_card_back(String id_card_back) {
    this.id_card_back = id_card_back;
  }
  public user_profile with_id_card_back(String id_card_back) {
    this.id_card_back = id_card_back;
    return this;
  }
  private String id_card_handheld;
  public String get_id_card_handheld() {
    return id_card_handheld;
  }
  public void set_id_card_handheld(String id_card_handheld) {
    this.id_card_handheld = id_card_handheld;
  }
  public user_profile with_id_card_handheld(String id_card_handheld) {
    this.id_card_handheld = id_card_handheld;
    return this;
  }
  private String area;
  public String get_area() {
    return area;
  }
  public void set_area(String area) {
    this.area = area;
  }
  public user_profile with_area(String area) {
    this.area = area;
    return this;
  }
  private String company;
  public String get_company() {
    return company;
  }
  public void set_company(String company) {
    this.company = company;
  }
  public user_profile with_company(String company) {
    this.company = company;
    return this;
  }
  private String career;
  public String get_career() {
    return career;
  }
  public void set_career(String career) {
    this.career = career;
  }
  public user_profile with_career(String career) {
    this.career = career;
    return this;
  }
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof user_profile)) {
      return false;
    }
    user_profile that = (user_profile) o;
    boolean equal = true;
    equal = equal && (this.user_id == null ? that.user_id == null : this.user_id.equals(that.user_id));
    equal = equal && (this.gender == null ? that.gender == null : this.gender.equals(that.gender));
    equal = equal && (this.birthday == null ? that.birthday == null : this.birthday.equals(that.birthday));
    equal = equal && (this.real_name == null ? that.real_name == null : this.real_name.equals(that.real_name));
    equal = equal && (this.create_time == null ? that.create_time == null : this.create_time.equals(that.create_time));
    equal = equal && (this.update_time == null ? that.update_time == null : this.update_time.equals(that.update_time));
    equal = equal && (this.register_media_time == null ? that.register_media_time == null : this.register_media_time.equals(that.register_media_time));
    equal = equal && (this.id_number == null ? that.id_number == null : this.id_number.equals(that.id_number));
    equal = equal && (this.id_card_front == null ? that.id_card_front == null : this.id_card_front.equals(that.id_card_front));
    equal = equal && (this.id_card_back == null ? that.id_card_back == null : this.id_card_back.equals(that.id_card_back));
    equal = equal && (this.id_card_handheld == null ? that.id_card_handheld == null : this.id_card_handheld.equals(that.id_card_handheld));
    equal = equal && (this.area == null ? that.area == null : this.area.equals(that.area));
    equal = equal && (this.company == null ? that.company == null : this.company.equals(that.company));
    equal = equal && (this.career == null ? that.career == null : this.career.equals(that.career));
    return equal;
  }
  public boolean equals0(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof user_profile)) {
      return false;
    }
    user_profile that = (user_profile) o;
    boolean equal = true;
    equal = equal && (this.user_id == null ? that.user_id == null : this.user_id.equals(that.user_id));
    equal = equal && (this.gender == null ? that.gender == null : this.gender.equals(that.gender));
    equal = equal && (this.birthday == null ? that.birthday == null : this.birthday.equals(that.birthday));
    equal = equal && (this.real_name == null ? that.real_name == null : this.real_name.equals(that.real_name));
    equal = equal && (this.create_time == null ? that.create_time == null : this.create_time.equals(that.create_time));
    equal = equal && (this.update_time == null ? that.update_time == null : this.update_time.equals(that.update_time));
    equal = equal && (this.register_media_time == null ? that.register_media_time == null : this.register_media_time.equals(that.register_media_time));
    equal = equal && (this.id_number == null ? that.id_number == null : this.id_number.equals(that.id_number));
    equal = equal && (this.id_card_front == null ? that.id_card_front == null : this.id_card_front.equals(that.id_card_front));
    equal = equal && (this.id_card_back == null ? that.id_card_back == null : this.id_card_back.equals(that.id_card_back));
    equal = equal && (this.id_card_handheld == null ? that.id_card_handheld == null : this.id_card_handheld.equals(that.id_card_handheld));
    equal = equal && (this.area == null ? that.area == null : this.area.equals(that.area));
    equal = equal && (this.company == null ? that.company == null : this.company.equals(that.company));
    equal = equal && (this.career == null ? that.career == null : this.career.equals(that.career));
    return equal;
  }
  public void readFields(ResultSet __dbResults) throws SQLException {
    this.__cur_result_set = __dbResults;
    this.user_id = JdbcWritableBridge.readLong(1, __dbResults);
    this.gender = JdbcWritableBridge.readBoolean(2, __dbResults);
    this.birthday = JdbcWritableBridge.readDate(3, __dbResults);
    this.real_name = JdbcWritableBridge.readString(4, __dbResults);
    this.create_time = JdbcWritableBridge.readTimestamp(5, __dbResults);
    this.update_time = JdbcWritableBridge.readTimestamp(6, __dbResults);
    this.register_media_time = JdbcWritableBridge.readTimestamp(7, __dbResults);
    this.id_number = JdbcWritableBridge.readString(8, __dbResults);
    this.id_card_front = JdbcWritableBridge.readString(9, __dbResults);
    this.id_card_back = JdbcWritableBridge.readString(10, __dbResults);
    this.id_card_handheld = JdbcWritableBridge.readString(11, __dbResults);
    this.area = JdbcWritableBridge.readString(12, __dbResults);
    this.company = JdbcWritableBridge.readString(13, __dbResults);
    this.career = JdbcWritableBridge.readString(14, __dbResults);
  }
  public void readFields0(ResultSet __dbResults) throws SQLException {
    this.user_id = JdbcWritableBridge.readLong(1, __dbResults);
    this.gender = JdbcWritableBridge.readBoolean(2, __dbResults);
    this.birthday = JdbcWritableBridge.readDate(3, __dbResults);
    this.real_name = JdbcWritableBridge.readString(4, __dbResults);
    this.create_time = JdbcWritableBridge.readTimestamp(5, __dbResults);
    this.update_time = JdbcWritableBridge.readTimestamp(6, __dbResults);
    this.register_media_time = JdbcWritableBridge.readTimestamp(7, __dbResults);
    this.id_number = JdbcWritableBridge.readString(8, __dbResults);
    this.id_card_front = JdbcWritableBridge.readString(9, __dbResults);
    this.id_card_back = JdbcWritableBridge.readString(10, __dbResults);
    this.id_card_handheld = JdbcWritableBridge.readString(11, __dbResults);
    this.area = JdbcWritableBridge.readString(12, __dbResults);
    this.company = JdbcWritableBridge.readString(13, __dbResults);
    this.career = JdbcWritableBridge.readString(14, __dbResults);
  }
  public void loadLargeObjects(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void loadLargeObjects0(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void write(PreparedStatement __dbStmt) throws SQLException {
    write(__dbStmt, 0);
  }

  public int write(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeLong(user_id, 1 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeBoolean(gender, 2 + __off, -7, __dbStmt);
    JdbcWritableBridge.writeDate(birthday, 3 + __off, 91, __dbStmt);
    JdbcWritableBridge.writeString(real_name, 4 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeTimestamp(create_time, 5 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(update_time, 6 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(register_media_time, 7 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(id_number, 8 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(id_card_front, 9 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(id_card_back, 10 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(id_card_handheld, 11 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(area, 12 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(company, 13 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(career, 14 + __off, 12, __dbStmt);
    return 14;
  }
  public void write0(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeLong(user_id, 1 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeBoolean(gender, 2 + __off, -7, __dbStmt);
    JdbcWritableBridge.writeDate(birthday, 3 + __off, 91, __dbStmt);
    JdbcWritableBridge.writeString(real_name, 4 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeTimestamp(create_time, 5 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(update_time, 6 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(register_media_time, 7 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(id_number, 8 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(id_card_front, 9 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(id_card_back, 10 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(id_card_handheld, 11 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(area, 12 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(company, 13 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(career, 14 + __off, 12, __dbStmt);
  }
  public void readFields(DataInput __dataIn) throws IOException {
this.readFields0(__dataIn);  }
  public void readFields0(DataInput __dataIn) throws IOException {
    if (__dataIn.readBoolean()) { 
        this.user_id = null;
    } else {
    this.user_id = Long.valueOf(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.gender = null;
    } else {
    this.gender = Boolean.valueOf(__dataIn.readBoolean());
    }
    if (__dataIn.readBoolean()) { 
        this.birthday = null;
    } else {
    this.birthday = new Date(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.real_name = null;
    } else {
    this.real_name = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.create_time = null;
    } else {
    this.create_time = new Timestamp(__dataIn.readLong());
    this.create_time.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.update_time = null;
    } else {
    this.update_time = new Timestamp(__dataIn.readLong());
    this.update_time.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.register_media_time = null;
    } else {
    this.register_media_time = new Timestamp(__dataIn.readLong());
    this.register_media_time.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.id_number = null;
    } else {
    this.id_number = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.id_card_front = null;
    } else {
    this.id_card_front = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.id_card_back = null;
    } else {
    this.id_card_back = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.id_card_handheld = null;
    } else {
    this.id_card_handheld = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.area = null;
    } else {
    this.area = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.company = null;
    } else {
    this.company = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.career = null;
    } else {
    this.career = Text.readString(__dataIn);
    }
  }
  public void write(DataOutput __dataOut) throws IOException {
    if (null == this.user_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.user_id);
    }
    if (null == this.gender) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeBoolean(this.gender);
    }
    if (null == this.birthday) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.birthday.getTime());
    }
    if (null == this.real_name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, real_name);
    }
    if (null == this.create_time) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.create_time.getTime());
    __dataOut.writeInt(this.create_time.getNanos());
    }
    if (null == this.update_time) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.update_time.getTime());
    __dataOut.writeInt(this.update_time.getNanos());
    }
    if (null == this.register_media_time) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.register_media_time.getTime());
    __dataOut.writeInt(this.register_media_time.getNanos());
    }
    if (null == this.id_number) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_number);
    }
    if (null == this.id_card_front) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_card_front);
    }
    if (null == this.id_card_back) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_card_back);
    }
    if (null == this.id_card_handheld) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_card_handheld);
    }
    if (null == this.area) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, area);
    }
    if (null == this.company) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, company);
    }
    if (null == this.career) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, career);
    }
  }
  public void write0(DataOutput __dataOut) throws IOException {
    if (null == this.user_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.user_id);
    }
    if (null == this.gender) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeBoolean(this.gender);
    }
    if (null == this.birthday) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.birthday.getTime());
    }
    if (null == this.real_name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, real_name);
    }
    if (null == this.create_time) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.create_time.getTime());
    __dataOut.writeInt(this.create_time.getNanos());
    }
    if (null == this.update_time) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.update_time.getTime());
    __dataOut.writeInt(this.update_time.getNanos());
    }
    if (null == this.register_media_time) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.register_media_time.getTime());
    __dataOut.writeInt(this.register_media_time.getNanos());
    }
    if (null == this.id_number) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_number);
    }
    if (null == this.id_card_front) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_card_front);
    }
    if (null == this.id_card_back) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_card_back);
    }
    if (null == this.id_card_handheld) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, id_card_handheld);
    }
    if (null == this.area) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, area);
    }
    if (null == this.company) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, company);
    }
    if (null == this.career) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, career);
    }
  }
  private static final DelimiterSet __outputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  public String toString() {
    return toString(__outputDelimiters, true);
  }
  public String toString(DelimiterSet delimiters) {
    return toString(delimiters, true);
  }
  public String toString(boolean useRecordDelim) {
    return toString(__outputDelimiters, useRecordDelim);
  }
  public String toString(DelimiterSet delimiters, boolean useRecordDelim) {
    StringBuilder __sb = new StringBuilder();
    char fieldDelim = delimiters.getFieldsTerminatedBy();
    __sb.append(FieldFormatter.escapeAndEnclose(user_id==null?"null":"" + user_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(gender==null?"null":"" + gender, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(birthday==null?"null":"" + birthday, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(real_name==null?"null":real_name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(create_time==null?"null":"" + create_time, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(update_time==null?"null":"" + update_time, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(register_media_time==null?"null":"" + register_media_time, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_number==null?"null":id_number, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_card_front==null?"null":id_card_front, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_card_back==null?"null":id_card_back, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_card_handheld==null?"null":id_card_handheld, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(area==null?"null":area, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(company==null?"null":company, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(career==null?"null":career, delimiters));
    if (useRecordDelim) {
      __sb.append(delimiters.getLinesTerminatedBy());
    }
    return __sb.toString();
  }
  public void toString0(DelimiterSet delimiters, StringBuilder __sb, char fieldDelim) {
    __sb.append(FieldFormatter.escapeAndEnclose(user_id==null?"null":"" + user_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(gender==null?"null":"" + gender, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(birthday==null?"null":"" + birthday, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(real_name==null?"null":real_name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(create_time==null?"null":"" + create_time, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(update_time==null?"null":"" + update_time, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(register_media_time==null?"null":"" + register_media_time, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_number==null?"null":id_number, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_card_front==null?"null":id_card_front, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_card_back==null?"null":id_card_back, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(id_card_handheld==null?"null":id_card_handheld, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(area==null?"null":area, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(company==null?"null":company, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(career==null?"null":career, delimiters));
  }
  private static final DelimiterSet __inputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  private RecordParser __parser;
  public void parse(Text __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharSequence __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(byte [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(char [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(ByteBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  private void __loadFromFields(List<String> fields) {
    Iterator<String> __it = fields.listIterator();
    String __cur_str = null;
    try {
    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.user_id = null; } else {
      this.user_id = Long.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.gender = null; } else {
      this.gender = BooleanParser.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.birthday = null; } else {
      this.birthday = java.sql.Date.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.real_name = null; } else {
      this.real_name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.create_time = null; } else {
      this.create_time = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.update_time = null; } else {
      this.update_time = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.register_media_time = null; } else {
      this.register_media_time = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_number = null; } else {
      this.id_number = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_card_front = null; } else {
      this.id_card_front = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_card_back = null; } else {
      this.id_card_back = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_card_handheld = null; } else {
      this.id_card_handheld = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.area = null; } else {
      this.area = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.company = null; } else {
      this.company = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.career = null; } else {
      this.career = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  private void __loadFromFields0(Iterator<String> __it) {
    String __cur_str = null;
    try {
    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.user_id = null; } else {
      this.user_id = Long.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.gender = null; } else {
      this.gender = BooleanParser.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.birthday = null; } else {
      this.birthday = java.sql.Date.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.real_name = null; } else {
      this.real_name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.create_time = null; } else {
      this.create_time = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.update_time = null; } else {
      this.update_time = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.register_media_time = null; } else {
      this.register_media_time = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_number = null; } else {
      this.id_number = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_card_front = null; } else {
      this.id_card_front = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_card_back = null; } else {
      this.id_card_back = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.id_card_handheld = null; } else {
      this.id_card_handheld = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.area = null; } else {
      this.area = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.company = null; } else {
      this.company = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.career = null; } else {
      this.career = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  public Object clone() throws CloneNotSupportedException {
    user_profile o = (user_profile) super.clone();
    o.birthday = (o.birthday != null) ? (java.sql.Date) o.birthday.clone() : null;
    o.create_time = (o.create_time != null) ? (java.sql.Timestamp) o.create_time.clone() : null;
    o.update_time = (o.update_time != null) ? (java.sql.Timestamp) o.update_time.clone() : null;
    o.register_media_time = (o.register_media_time != null) ? (java.sql.Timestamp) o.register_media_time.clone() : null;
    return o;
  }

  public void clone0(user_profile o) throws CloneNotSupportedException {
    o.birthday = (o.birthday != null) ? (java.sql.Date) o.birthday.clone() : null;
    o.create_time = (o.create_time != null) ? (java.sql.Timestamp) o.create_time.clone() : null;
    o.update_time = (o.update_time != null) ? (java.sql.Timestamp) o.update_time.clone() : null;
    o.register_media_time = (o.register_media_time != null) ? (java.sql.Timestamp) o.register_media_time.clone() : null;
  }

  public Map<String, Object> getFieldMap() {
    Map<String, Object> __sqoop$field_map = new HashMap<String, Object>();
    __sqoop$field_map.put("user_id", this.user_id);
    __sqoop$field_map.put("gender", this.gender);
    __sqoop$field_map.put("birthday", this.birthday);
    __sqoop$field_map.put("real_name", this.real_name);
    __sqoop$field_map.put("create_time", this.create_time);
    __sqoop$field_map.put("update_time", this.update_time);
    __sqoop$field_map.put("register_media_time", this.register_media_time);
    __sqoop$field_map.put("id_number", this.id_number);
    __sqoop$field_map.put("id_card_front", this.id_card_front);
    __sqoop$field_map.put("id_card_back", this.id_card_back);
    __sqoop$field_map.put("id_card_handheld", this.id_card_handheld);
    __sqoop$field_map.put("area", this.area);
    __sqoop$field_map.put("company", this.company);
    __sqoop$field_map.put("career", this.career);
    return __sqoop$field_map;
  }

  public void getFieldMap0(Map<String, Object> __sqoop$field_map) {
    __sqoop$field_map.put("user_id", this.user_id);
    __sqoop$field_map.put("gender", this.gender);
    __sqoop$field_map.put("birthday", this.birthday);
    __sqoop$field_map.put("real_name", this.real_name);
    __sqoop$field_map.put("create_time", this.create_time);
    __sqoop$field_map.put("update_time", this.update_time);
    __sqoop$field_map.put("register_media_time", this.register_media_time);
    __sqoop$field_map.put("id_number", this.id_number);
    __sqoop$field_map.put("id_card_front", this.id_card_front);
    __sqoop$field_map.put("id_card_back", this.id_card_back);
    __sqoop$field_map.put("id_card_handheld", this.id_card_handheld);
    __sqoop$field_map.put("area", this.area);
    __sqoop$field_map.put("company", this.company);
    __sqoop$field_map.put("career", this.career);
  }

  public void setField(String __fieldName, Object __fieldVal) {
    if (!setters.containsKey(__fieldName)) {
      throw new RuntimeException("No such field:"+__fieldName);
    }
    setters.get(__fieldName).setField(__fieldVal);
  }

}
